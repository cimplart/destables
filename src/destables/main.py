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

import struct
from tkinter.tix import COLUMN
from xmlrpc.client import boolean
import PySimpleGUI as sg
from tabulate import tabulate
import re
import clipboard
import tabhelper

def hidable(layout, key):
    return sg.pin(sg.Column(layout, key=key))

def show_inner_table(initial_values, header, required_cols):

    result = initial_values

    MAX_ROWS = 16
    MAX_COL = len(header)

    inner_layout = [ [ sg.Input(size=(20, 1), pad=(1,1), justification='right', key=str(i)+','+str(j), enable_events=True)
                      for j in range(MAX_COL) ] for i in range(MAX_ROWS) ]

    column_layout = [ [ hidable([ inner_layout[row] ], key=row) ] for row in range(MAX_ROWS) ]

    layout = [ [ sg.Text(header[i], size=(20, 1)) for i in range(len(header)) ],
               [ sg.Col(column_layout, scrollable=True) ],
               [ sg.Push(), sg.Ok(size=(15, 1)), sg.Cancel(size=(15, 1)) ] ]

    window = sg.Window('Add feature elements', layout, finalize=True)

    for row in range(len(initial_values)):
        for col in range(MAX_COL):
            window[str(row)+','+str(col)].update(value=initial_values[row][col])

    for row in range(MAX_ROWS):
        if row > len(initial_values):
            window[row].update(visible=False)
        for col in range(MAX_COL):
            window[str(row)+','+str(col)].bind("<Return>", "_RETURN")
    last_visible_row = len(initial_values)
    window[str(last_visible_row)+',0'].set_focus()

    while True:
        event, values = window.read()

        if event != None and isinstance(event, str):
            m = re.match(r'([0-9]+),([0-9]+)_RETURN', event)
            if m != None:
                row = m.group(1)
                col = m.group(2)
                has_val = [ values[row+','+str(c)] != '' or c not in required_cols for c in range(MAX_COL) ]
                if all(has_val) and int(row) < MAX_ROWS-1:
                    #show next row if current row is filled in
                    last_visible_row = int(row)+1
                    window[last_visible_row].update(visible=True)
                    window[str(int(row)+1)+',0'].set_focus()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'Ok':
            result = []
            for row in range(last_visible_row+1):
                col_values = []
                for col in range(MAX_COL):
                    col_values.append(values[str(row)+','+str(col)])
                #Required entries must not be empty.
                if all([ col_values[c] != '' or c not in required_cols for c in range(MAX_COL) ]):
                    result.append(col_values)
            break

    window.close()
    print(result)
    return result

def show_type_table():

    fields = [ 'Type name:', 'Description:', 'Kind:', 'Declared in:', 'Type:', 'Elements:', 'Constants:' ]
    kinds = [ 'Typedef', 'Structure', 'Enumeration' ]

    inputs = [
        sg.InputText(key=fields[0], size=(64, 1)),
        sg.Multiline(key=fields[1], enter_submits=False, autoscroll=True, size=(64, 2)),
        sg.Combo(kinds, kinds[1], key=fields[2], enable_events=True, readonly=True, size=(32, 1)),
        sg.InputText(key=fields[3], size=(32, 1)),
        sg.Multiline(key=fields[4], enter_submits=False, autoscroll=True, enable_events=True, size=(64, 1))
    ]

    typedef_row = [ [ sg.Text(fields[4]), sg.Push(), inputs[4]] ]
    struct_row = [ [ sg.Text(fields[5]), sg.Text('None', key='struct-fields', size=(48, 1)),
                     sg.Button('Edit elements', key='edit-elements', enable_events=True) ] ]
    enum_row = [ [ sg.Text(fields[6]), sg.Text('None', key='enum-values', size=(48, 1)),
                     sg.Button('Edit enum constants', key='edit-constants', enable_events=True) ] ]

    layout = [
                ([ sg.Text(fields[i]), sg.Push(), inputs[i] ] for i in range(4)),
                [ hidable(typedef_row, key='typedef-row')],
                [ hidable(struct_row, key='struct-row') ],
                [ hidable(enum_row, key='enum-row')],
                [ sg.HorizontalSeparator() ],
                [ sg.Push(), sg.Button('Clear', key='clear'), sg.Button('Copy table to clipboard', key='copy'),
                  sg.Button('Copy to clipboard & close', key='copy&close') ]
             ]

    clearable_keys = [ k for k in fields[0:4] if k != 'Kind:' ] + [ 'struct-fields', 'enum-values']

    window = sg.Window('Fill in type table', layout, finalize=True)

    code_indent = '\n   '
    code_cell = inputs[4]
    code_cell.update(' .. code-block::' + code_indent)
    code_cell.bind("<Return>", "RETURN")

    window['typedef-row'].update(visible=False)
    window['enum-row'].update(visible=False)

    struct_elements = [ ]
    enum_constants = [ ]

    while True:
        event, values = window.read()
        print(event, values)

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
            header = [fields[0], values[fields[0]]]
            table = [ [ fields[i], values[fields[i]] ] for i in range(1, 4) ]
            if values['Kind:'] == 'Typedef':
                table.extend([ [ fields[4], values[fields[4]] ] ])
            elif values['Kind:'] == 'Structure':
                nested_table = None
                if len(struct_elements) > 0:
                    nested_table = tabulate(struct_elements, tablefmt="grid")
                    table.extend([ [ fields[5], nested_table ] ])
                else:
                    table.extend([ [ fields[5], 'None' ] ])
            elif values['Kind:'] == 'Enumeration':
                nested_table = None
                if len(enum_constants) > 0:
                    nested_table = tabulate(enum_constants, tablefmt="grid")
                    table.extend([ [ fields[6], nested_table ] ])
                else:
                    table.extend([ [ fields[6], 'None' ] ])
            table_str = tabulate(table, headers=header, tablefmt="grid")
            if values['Kind:'] == 'Structure' and nested_table != None:
                table_str = tabhelper.merge_nested_tables({ fields[5] : nested_table }, table_str)
            elif values['Kind:'] == 'Enumeration' and nested_table != None:
                table_str = tabhelper.merge_nested_tables({ fields[6] : nested_table }, table_str)

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
            struct_elements = show_inner_table(struct_elements, ['Type:', 'Name:', 'Description:'], required_cols=[0, 1, 2])
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
            enum_constants = show_inner_table(enum_constants, ['Constant:', 'Initial value:', 'Description:'], required_cols=[0, 2])
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

def main():

    layout = [[ sg.Button('Type table', key='type', size = (30, 2)) ],
              [ sg.Button('Function table', key='function', size = (30, 2)) ],
              [ sg.Button('Variables table', key='variables', size = (30, 2)) ],
              [ sg.Button('Macro constants table', key='macro-constants', size = (30, 2)) ],
              [ sg.Button('Macro function table', key='macro-function', size = (30, 2)) ],
              [ sg.HorizontalSeparator() ],
              [ sg.Button('Exit', size = (30, 3))] ]

    window = sg.Window('SW Design Tables Tool', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'type':
            show_type_table()
        elif event == 'function':
            pass #TODO

    window.close()

if __name__ == "__main__":
    main()
