#
# destables
# Copyright (C) 2022  Arthur Wisz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import PySimpleGUI as sg
from commonwin import *
import clipboard
import tabhelper
from tabulate import tabulate
from c11tools import *

TYPE_NAME = 'Type name:'
DESCRIPTION = 'Description:'
KIND = 'Kind:'
HEADER = 'Declared in:'
TYPEDEF = 'Type:'
ELEMENTS = 'Elements:'
CONSTANTS = 'Constants:'

def show_type_table():

    kinds = [ 'Typedef', 'Structure', 'Enumeration' ]

    inputs = [
        sg.InputText(key=TYPE_NAME, size=(64, 1)),
        sg.Multiline(key=DESCRIPTION, enter_submits=False, autoscroll=True, size=(64, 2)),
        sg.Combo(kinds, kinds[0], key=KIND, enable_events=True, readonly=True, size=(32, 1)),
        sg.InputText(key=HEADER, size=(32, 1)),
        sg.Multiline(key=TYPEDEF, enter_submits=False, autoscroll=True, enable_events=True, size=(64, 1))
    ]

    typedef_row = [ [ sg.Text(TYPEDEF, key=TYPEDEF+'-label'), sg.Push(), inputs[4]] ]
    struct_row = [ [ sg.Text(ELEMENTS), sg.Text('None', key='struct-fields', size=(48, 1)),
                     sg.Button('Edit elements', key='edit-elements', enable_events=True) ] ]
    enum_row = [ [ sg.Text(CONSTANTS), sg.Text('None', key='enum-values', size=(48, 1)),
                     sg.Button('Edit enum constants', key='edit-constants', enable_events=True) ] ]

    layout = [
        ([ sg.Text([ TYPE_NAME, DESCRIPTION, KIND, HEADER ][i], k=[ TYPE_NAME, DESCRIPTION, KIND, HEADER ][i]+'-label'),
           sg.Push(), inputs[i] ] for i in range(4)),
                [ hidable(typedef_row, key='typedef-row')],
                [ hidable(struct_row, key='struct-row') ],
                [ hidable(enum_row, key='enum-row')],
                [ sg.HorizontalSeparator() ],
                [ sg.Text('', key='status', size=(48,1), text_color='red'), sg.Push(),
                        sg.Button('Clear', key='clear'), sg.Button('Copy table to clipboard', key='copy'),
                        sg.Button('Close', key='close') ]
             ]

    clearable_keys = [ TYPE_NAME, DESCRIPTION, HEADER, TYPEDEF ] + [ 'struct-fields', 'enum-values']

    window = sg.Window('Fill in type table', layout, finalize=True)

    code_indent = '\n   '
    code_cell = inputs[4]
    code_cell.update(' .. code-block::' + code_indent)
    code_cell.bind("<Return>", "RETURN")

    window['struct-row'].update(visible=False)
    window['enum-row'].update(visible=False)

    struct_elements = [ ]
    enum_constants = [ ]

    simply_checked_keys = [ TYPE_NAME, DESCRIPTION, HEADER ]

    inner_table_col_width = [ 32, 32, 64]

    while True:
        event, values = window.read()
        #print(event, values)

        if event == sg.WIN_CLOSED:
            break

        if event == 'clear':
            for k in clearable_keys:
                window[k]('')
            code_cell.update(' .. code-block::' + code_indent)
            struct_elements = [ ]
            enum_constants = [ ]
            window['struct-fields']('None')
            window['enum-values']('None')
        elif 'copy' in event:

            if not _is_input_valid(values, window, simply_checked_keys):
                continue

            table_str = _render_table(values, struct_elements, enum_constants)

            print(table_str)
            clipboard.copy(table_str)
        elif 'RETURN' in event:
            code_cell.update(code_cell.get() + code_indent)
        elif 'Kind' in event:
            if values['Kind:'] == 'Structure':
                window['typedef-row'].update(visible=False)
                window['enum-row'].update(visible=False)
                window['struct-row'].update(visible=True)
            elif values['Kind:'] == 'Typedef':
                window['struct-row'].update(visible=False)
                window['enum-row'].update(visible=False)
                window['typedef-row'].update(visible=True)
            elif values['Kind:'] == 'Enumeration':
                window['struct-row'].update(visible=False)
                window['typedef-row'].update(visible=False)
                window['enum-row'].update(visible=True)
        elif event == 'edit-elements':
            struct_elements = show_inner_table(struct_elements, ['Type:', 'Name:', 'Description:'],
                                               required_cols=[0, 1, 2], col_width = inner_table_col_width)
            struct_fields = ''
            for row in range(len(struct_elements)):
                struct_fields += struct_elements[row][1] + ','
            if not struct_fields:
                struct_fields = 'None'
            else:
                struct_fields = struct_fields[:-1]  #strip last ','
                if len(struct_fields) > 64:
                    struct_fields = struct_fields[:64] + '...'
            window['struct-fields'].update(struct_fields)
        elif event == 'edit-constants':
            enum_constants = show_inner_table(enum_constants, ['Constant:', 'Initial value:', 'Description:'],
                                              required_cols=[0, 2], col_width=inner_table_col_width)
            enum_idents = ''
            for row in range(len(enum_constants)):
                enum_idents += enum_constants[row][0] + ','
            if not enum_idents:
                enum_idents = 'None'
            else:
                enum_idents = enum_idents[:-1]  #strip last ','
                if len(enum_idents) > 64:
                    enum_idents = enum_idents[:64] + '...'
            window['enum-values'].update(enum_idents)

        if 'close' in event:
            break

    window.close()

def _is_input_valid(values, window, simply_checked_keys) -> bool:

    is_input_valid = True

    # Simple checks.
    window['status'].update('')
    for k in simply_checked_keys:
        if not values[k]:
            window[k+'-label'].update(text_color='red')
            is_input_valid = False
        else:
            window[k+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    if values[KIND] == 'Typedef':
        try:
            type_name = get_typedef_name(values[TYPEDEF])
            window[TYPEDEF+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)
        except Exception as e:
            print('C parser exception: ', str(e))
            window['status'].update('Invalid syntax')
            window[TYPEDEF+'-label'].update(text_color='red')
            return False

        if type_name is None:
            window['status'].update('Invalid typedef syntax')
            window[TYPEDEF+'-label'].update(text_color='red')
            window[TYPE_NAME+'-label'].update(text_color='red')
            return False

        if type_name != values[TYPE_NAME]:
            window['status'].update('Type name mismatch')
            window[TYPEDEF+'-label'].update(text_color='red')
            window[TYPE_NAME+'-label'].update(text_color='red')
            return False
        else:
            window[TYPEDEF+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)
            window[TYPE_NAME+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    return is_input_valid


def _render_table(values, struct_elements, enum_constants):

    # Create the table.
    header = [TYPE_NAME, values[TYPE_NAME]]
    table = [ [ DESCRIPTION, values[DESCRIPTION] ],
              [ KIND, values[KIND] ],
              [ HEADER, values[HEADER] ] ]
    if values[KIND] == 'Typedef':
        table.extend([ [ TYPEDEF, values[TYPEDEF] ] ])
    elif values[KIND] == 'Structure':
        nested_table = None
        if len(struct_elements) > 0:
            nested_table = tabulate(struct_elements, tablefmt="grid")
            table.extend([ [ ELEMENTS, nested_table ] ])
        else:
            table.extend([ [ ELEMENTS, 'None' ] ])
    elif values[KIND] == 'Enumeration':
        nested_table = None
        if len(enum_constants) > 0:
            nested_table = tabulate(enum_constants, tablefmt="grid")
            table.extend([ [ CONSTANTS, nested_table ] ])
        else:
            table.extend([ [ CONSTANTS, 'None' ] ])

    table_str = tabulate(table, headers=header, tablefmt="grid")

    if values[KIND] == 'Structure' and nested_table != None:
        table_str = tabhelper.merge_nested_tables({ ELEMENTS : nested_table }, table_str)
    elif values[KIND] == 'Enumeration' and nested_table != None:
        table_str = tabhelper.merge_nested_tables({ CONSTANTS : nested_table }, table_str)

    return table_str
