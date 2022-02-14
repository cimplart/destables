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
from c99tools import *

def _get_func_params(syntax):
    decl = syntax.replace('.. code-block::', '')
    decl = decl.replace('\n', ' ')
    decl = decl.strip() + ';'
    return get_func_params(decl)

def _get_func_name(syntax):
    decl = syntax.replace('.. code-block::', '')
    decl = decl.replace('\n', ' ')
    decl = decl.strip() + ';'
    return get_func_name(decl)

def show_function_table():

    FUNC_NAME = 'Function name:'
    DESCRIPTION = 'Description:'
    SYNTAX = 'Syntax:'
    HEADER = 'Declared in:'
    ISR = 'May be called from ISR:'
    REENTRANT = 'Reentrancy:'
    RETURN = 'Return value:'
    IN_PARAMS = 'Parameters [in]:'
    OUT_PARAMS = 'Parameters [out]:'
    IN_OUT_PARAMS = 'Parameters [in-out]:'
    CALL_CYCLE = 'Call cycle interval:'

    inputs = [
        sg.Input(key=FUNC_NAME, size=(48, 1)),
        sg.Multiline(key=DESCRIPTION, enter_submits=False, autoscroll=True, size=(64, 2)),
        sg.Multiline(key=SYNTAX, enter_submits=False, autoscroll=True, enable_events=True, size=(64, 5)),
        sg.Input(key=HEADER, size=(32, 1)),
    ]

    layout = [
        ([ sg.Text([ FUNC_NAME, DESCRIPTION, SYNTAX, HEADER ][i]), sg.Push(), inputs[i] ] for i in range(4)),
        [ sg.Checkbox(text=ISR, key=ISR) ],
        [ sg.Checkbox(text=REENTRANT, key=REENTRANT) ],
        [ sg.Text(RETURN), sg.Push(), sg.Input('void', key='retval-type', size=(32,1)), sg.Input(key='retval-description', size=(64,1)) ],
        [ sg.Text(IN_PARAMS), sg.Text('None', key='in-params', size=(48, 1)), sg.Push(), sg.Button('Edit input parameters', key='edit-in-params', enable_events=True) ],
        [ sg.Text(OUT_PARAMS), sg.Text('None', key='out-params', size=(48, 1)), sg.Push(), sg.Button('Edit output parameters', key='edit-out-params', enable_events=True) ],
        [ sg.Text(IN_OUT_PARAMS), sg.Text('None', key='inout-params', size=(48, 1)), sg.Push(), sg.Button('Edit in-out parameters', key='edit-inout-params', enable_events=True) ],
        [ sg.Checkbox(text='Is cyclic', key='is-cyclic', enable_events=True), sg.Push(), sg.Text(CALL_CYCLE), sg.Input(key=CALL_CYCLE) ],
        [ sg.HorizontalSeparator() ],
        [ sg.Text('', key='status', size=(48,1), text_color='red'), sg.Push(),
                sg.Button('Clear', key='clear'), sg.Button('Copy table to clipboard', key='copy'),
                sg.Button('Copy to clipboard & close', key='copy&close') ]
    ]

    clearable_keys = [ FUNC_NAME, DESCRIPTION, SYNTAX, HEADER, ISR, REENTRANT, RETURN,
                       IN_PARAMS, OUT_PARAMS, IN_OUT_PARAMS, CALL_CYCLE ]

    window = sg.Window('Fill in function table', layout, finalize=True)

    code_indent = '\n   '
    code_cell = inputs[2]
    code_cell.update(' .. code-block::' + code_indent)
    code_cell.bind("<Return>", "RETURN")

    window[CALL_CYCLE].update(disabled=True)

    params_dict = {
        'in-params': [],
        'out-params' : [],
        'inout-params' : []
    }

    while True:
        event, values = window.read()
        #print(event, values)

        if event == sg.WIN_CLOSED:
            break

        if event == 'clear':
            for k in clearable_keys:
                window[k]('')
            code_cell.update(' .. code-block::' + code_indent)
            for k in params_dict:
                params_dict[k] = []
            window['in-params']('None')
            window['out-params']('None')
            window['inout-params']('None')
        elif 'copy' in event:
            try:
                func_params = _get_func_params(values[SYNTAX])
            except Exception as e:
                window['status'].update('ERROR: invalid syntax')
                continue

            if _get_func_name(values[SYNTAX]) != values[FUNC_NAME].strip():
                window['status'].update('ERROR: function name mismatch')
                continue

            documented_params = []
            for k in params_dict:
                if len(params_dict[k]) > 0:
                    for par in params_dict[k]:
                        documented_params.append(par[0])
            undocumented_params = list(set(func_params) - set(documented_params))

            if len(undocumented_params) > 0:
                window['status'].update('WARNING: ' + str(len(undocumented_params)) + ' undocumented parameters')

            header = [ FUNC_NAME, values[FUNC_NAME]]
            table = [ [ DESCRIPTION, values[DESCRIPTION ] ],
                      [ SYNTAX, values[SYNTAX] ],
                      [ HEADER, values[HEADER] ]  ]
            table.append( [ ISR, 'Yes' if values[ISR] else 'No' ] )
            table.append( [ REENTRANT, 'Reentrant' if values[REENTRANT] else 'Non-reentrant' ] )

            nested_return_table = None
            if values['retval-type'] != 'void':
                retval = [ [ values['retval-type'], values['retval-description'] ] ]
                nested_return_table = tabulate(retval, tablefmt="grid")
                table.append( [ RETURN, nested_return_table ] )
            else:
                table.append( [ RETURN, 'None' ] )

            nested_params_tables = { 'in-params': None, 'out-params' : None, 'inout-params' : None   }
            params_headers = { 'in-params': IN_PARAMS, 'out-params' : OUT_PARAMS, 'inout-params' : IN_OUT_PARAMS }

            for i in [ 'in-params', 'out-params', 'inout-params' ]:
                if len(params_dict[i]) > 0:
                    nested_params_tables[i] = tabulate(params_dict[i], tablefmt="grid")
                    table.append([ params_headers[i], nested_params_tables[i] ])
                #else:
                #    table.append([ params_headers[i], 'None' ])

            if values['is-cyclic']:
                table.append( [ CALL_CYCLE, values[CALL_CYCLE] ] )

            table_str = tabulate(table, headers=header, tablefmt="grid")

            if nested_return_table != None:
                table_str = tabhelper.merge_nested_tables({ RETURN : nested_return_table }, table_str)

            for i in [ 'in-params', 'out-params', 'inout-params' ]:
                if nested_params_tables[i] != None:
                    table_str = tabhelper.merge_nested_tables({ params_headers[i] : nested_params_tables[i] }, table_str)

            print(table_str)
            clipboard.copy(table_str)
        elif 'RETURN' in event:
            code_cell.update(code_cell.get() + code_indent)
        elif event in [ 'edit-in-params', 'edit-out-params', 'edit-inout-params' ]:
            params_key = event.replace('edit-', '')
            params_dict[params_key] = show_inner_table(params_dict[params_key], ['Parameter:', 'Description:'],
                                                       required_cols=[0, 1], col_width = [ 32, 64 ])
            params_list = ''
            for row in range(len(params_dict[params_key])):
                params_list += params_dict[params_key][row][0] + ','
            if not params_list:
                params_list = 'None'
            else:
                params_list = params_list[:-1]  #strip last ','
                if len(params_list) > 64:
                    params_list = params_list[:64] + '...'
            window[event.replace('edit-', '')].update(params_list)
        elif event == 'is-cyclic':
            if not values['is-cyclic']:
                window[CALL_CYCLE].update('')
            window[CALL_CYCLE].update(disabled=not values['is-cyclic'])

        if 'close' in event:
            break

    window.close()
