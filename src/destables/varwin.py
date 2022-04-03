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

VAR_GROUP = 'Variables Group:'
HEADER = 'Declared in:'
VARIABLES = 'Variables:'
DESCRIPTION = 'Description:'
SYNTAX = 'Syntax:'

def show_variable_table():

    inputs = [
        sg.Input(key=VAR_GROUP, size=(48, 1), enable_events=True),
        sg.Input(key=HEADER, size=(32, 1), enable_events=True),
    ]

    layout = [
        ([ sg.Text([ VAR_GROUP, HEADER ][i], k=[ VAR_GROUP, HEADER ][i]+'-label'),
           sg.Push(), inputs[i] ] for i in range(2)),
        [ sg.Text(VARIABLES, k=VARIABLES+'-label'), sg.Text('', key='variables', size=(48, 1)), sg.Push(), sg.Button('Edit variables', key='edit-variables', enable_events=True) ],
        [ sg.HorizontalSeparator() ],
        [ sg.Text('', key='status', size=(48,1), text_color='red'), sg.Push(),
                sg.Button('Clear', key='clear'), sg.Button('Copy table to clipboard', key='copy'),
                sg.Button('Close', key='close') ]
    ]

    clearable_keys = [ VAR_GROUP, HEADER ]

    simply_checked_keys = [ VAR_GROUP, HEADER ]

    variables = []

    window = sg.Window('Fill in variables table', layout, finalize=True)

    while True:
        event, values = window.read()
        #print(event, values)

        if event == sg.WIN_CLOSED:
            break

        if event == 'clear':
            for k in clearable_keys:
                window[k]('')
            window['variables']('')
        elif 'copy' in event:
            window['status'].update('')

            if not _is_input_valid(values, window, simply_checked_keys, variables):
                continue

            table_str = _render_table(values, variables)

            print(table_str)
            clipboard.copy(table_str)
        elif event in [ 'edit-variables' ]:
            variables = show_inner_table(variables, [ SYNTAX, DESCRIPTION ],
                                                      required_cols=[0, 1], col_width = [ 48, 64 ])
            var_list = ''
            window['status'].update('')
            for row in range(len(variables)):
                try:
                    var_name = get_variable_name(variables[row][0])
                except Exception as e:
                    print('C parser exception: ', str(e))
                    window['status'].update('Invalid syntax')
                    var_name = ''
                var_list += var_name + ','
            if not var_list:
                var_list = 'None'
            else:
                var_list = var_list[:-1]  #strip last ','
                if len(var_list) > 64:
                    var_list = var_list[:64] + '...'
            window[event.replace('edit-', '')].update(var_list)

        if 'close' in event:
            break

    window.close()


def _is_input_valid(values, window, simply_checked_keys, vars) -> bool:

    is_input_valid = True
    window['status'].update('')
    for k in simply_checked_keys:
        if not values[k]:
            window[k+'-label'].update(text_color='red')
            is_input_valid = False
        else:
            window[k+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    if not is_input_valid:
        return False

    for i in range(len(vars)):
        try:
            var_name = get_variable_name(vars[i][0])
        except Exception as e:
            print("error parsing '", vars[i][0], "': ", str(e))
            window['status'].update("Invalid syntax of variable " + str(i))
            return False

    return len(vars) > 0

def _render_table(values, vars):

    header = [ VAR_GROUP, values[VAR_GROUP] ]
    table = [ [ HEADER, values[HEADER]] ]

    var_tab = []
    for i in range(0, len(vars)):
        var_tab.append([ DESCRIPTION, vars[i][1] ])
        syntax = " .. code-block::\n\n    " + vars[i][0]
        var_tab.append([ SYNTAX, syntax ])

    nested_table = tabulate(var_tab, tablefmt="grid")
    table.extend([ [ VARIABLES, nested_table ] ])

    table_str = tabulate(table, headers=header, tablefmt="grid")
    table_str = tabhelper.merge_nested_tables({ VARIABLES : nested_table }, table_str)
    return table_str