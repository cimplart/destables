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

SYNTAX_CODE_INDENT = '\n   '

def get_func_param_indent(syntax):
    lines = syntax.split('\n')
    for l in lines:
        par_pos = l.find('(')
        if par_pos > 0:
            return par_pos + 1
    return SYNTAX_CODE_INDENT.count(' ')

def show_function_table(indent_size, add_table_directive):

    inputs = [
        sg.Input(key=FUNC_NAME, size=(48, 1), enable_events=True),
        sg.Multiline(key=DESCRIPTION, enter_submits=False, autoscroll=True, size=(64, 2), enable_events=True),
        sg.Multiline(key=SYNTAX, enter_submits=False, autoscroll=True, enable_events=True, size=(80, 7)),
        sg.Input(key=HEADER, size=(32, 1), enable_events=True),
    ]

    layout = [
        ([ sg.Text([ FUNC_NAME, DESCRIPTION, SYNTAX, HEADER ][i], k=[ FUNC_NAME, DESCRIPTION, SYNTAX, HEADER ][i]+'-label'),
           sg.Push(), inputs[i] ] for i in range(4)),
        [ sg.Checkbox(text=ISR, key=ISR) ],
        [ sg.Checkbox(text=REENTRANT, key=REENTRANT) ],
        [ sg.Text(RETURN, k=RETURN+'-label'), sg.Push(), sg.Text('', key='retval-type', size=(32,1)), sg.Input(key='retval-description', size=(64,1)) ],
        [ sg.Text(IN_PARAMS, k=IN_PARAMS+'-label'), sg.Text('None', key='in-params', size=(48, 1)), sg.Push(), sg.Button('Edit input parameters', key='edit-in-params', enable_events=True) ],
        [ sg.Text(OUT_PARAMS, k=OUT_PARAMS+'-label'), sg.Text('None', key='out-params', size=(48, 1)), sg.Push(), sg.Button('Edit output parameters', key='edit-out-params', enable_events=True) ],
        [ sg.Text(IN_OUT_PARAMS, k=IN_OUT_PARAMS+'-label'), sg.Text('None', key='inout-params', size=(48, 1)), sg.Push(), sg.Button('Edit in-out parameters', key='edit-inout-params', enable_events=True) ],
        [ sg.Checkbox(text='Is cyclic', key='is-cyclic', enable_events=True), sg.Push(), sg.Text(CALL_CYCLE, k=CALL_CYCLE+'-label'), sg.Input(key=CALL_CYCLE, enable_events=True) ],
        [ sg.HorizontalSeparator() ],
        [ sg.Text('', key='status', size=(48,1), text_color='red'), sg.Push(),
                sg.Button('Clear', key='clear'), sg.Button('Copy table to clipboard', key='copy'),
                sg.Button('Close', key='close') ]
    ]

    clearable_keys = [ FUNC_NAME, DESCRIPTION, SYNTAX, HEADER, ISR, REENTRANT, RETURN,
                       IN_PARAMS, OUT_PARAMS, IN_OUT_PARAMS, CALL_CYCLE ]

    simply_checked_keys = [ FUNC_NAME, DESCRIPTION, HEADER ]

    window = sg.Window('Fill in function table', layout, finalize=True)

    code_cell = inputs[2]
    code_cell.update(' .. code-block::' + 2 * SYNTAX_CODE_INDENT)
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
            code_cell.update(' .. code-block::' + 2 * SYNTAX_CODE_INDENT)
            for k in params_dict:
                params_dict[k] = []
            window['in-params']('None')
            window['out-params']('None')
            window['inout-params']('None')
        elif 'copy' in event:

            if not _is_input_valid(values, window, simply_checked_keys, params_dict):
                continue

            table_str = _render_table(values, params_dict)
            table_str = tabhelper._decorate_table(table_str, indent_size, add_table_directive)

            print(table_str)
            clipboard.copy(table_str)
        elif 'RETURN' in event:
            if code_cell.get().find('\n') < 0:
                code_cell.update(code_cell.get() + 2 * SYNTAX_CODE_INDENT)
            else:
                code_cell.update(code_cell.get() + '\n' + get_func_param_indent(code_cell.get()) * ' ')
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
        elif event in simply_checked_keys + [ SYNTAX, CALL_CYCLE ]:
            window[event + '-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

        if 'close' in event:
            break

    window.close()


def _is_input_valid(values, window, simply_checked_keys, params_dict) -> bool:

    is_input_valid = True

    # Simple checks.
    window['status'].update('')
    for k in simply_checked_keys:
        if not values[k]:
            window[k+'-label'].update(text_color='red')
            is_input_valid = False
        else:
            window[k+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    if values['is-cyclic'] and not values[CALL_CYCLE]:
        window[CALL_CYCLE+'-label'].update(text_color='red')
        is_input_valid = False
    else:
        window[CALL_CYCLE+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    if not is_input_valid:
        return False

    # Check consistency of the input.
    try:
        func_name, func_params, func_result_type = get_func_info(values[SYNTAX])
        window[SYNTAX+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)
    except Exception as e:
        print('C parser exception: ', str(e))
        window['status'].update('Invalid syntax')
        window[SYNTAX+'-label'].update(text_color='red')
        return False

    if values[FUNC_NAME] == '' or func_name != values[FUNC_NAME].strip():
        window['status'].update('Function name mismatch')
        window[SYNTAX+'-label'].update(text_color='red')
        window[FUNC_NAME+'-label'].update(text_color='red')
        return False
    else:
        window[SYNTAX+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)
        window[FUNC_NAME+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    values['retval-type'] = func_result_type
    window['retval-type'](func_result_type)

    if values['retval-type'] != 'void' and not values['retval-description']:
        window[RETURN+'-label'].update(text_color='red')
        return False
    else:
        window[RETURN+'-label'].update(text_color=sg.DEFAULT_TEXT_COLOR)

    documented_params = []
    for k in params_dict:
        if len(params_dict[k]) > 0:
            for par in params_dict[k]:
                documented_params.append(par[0])
    undocumented_params = list(set(func_params) - set(documented_params))

    if len(undocumented_params) > 0:
        window['status'].update(str(len(undocumented_params)) + ' undocumented parameter(s)')
        return False

    params_missing_in_syntax = list(set(documented_params) - set(func_params))
    if len(params_missing_in_syntax) > 0:
        window[SYNTAX+'-label'].update(text_color='red')
        window['status'].update(str(len(params_missing_in_syntax)) + ' missing parameter(s) in function syntax')
        return False

    return True

def pad_value(value, width):
    if width - len(value) > 0:
        return value + '$' * (width - len(value))
    else:
        return value

def _render_table(values, params_dict):

    # Create the table.
    header = [ FUNC_NAME, values[FUNC_NAME]]
    table = [ [ DESCRIPTION, values[DESCRIPTION ] ],
                [ SYNTAX, values[SYNTAX] ],
                [ HEADER, values[HEADER] ]  ]
    table.append( [ ISR, 'Yes' if values[ISR] else 'No' ] )
    table.append( [ REENTRANT, 'Reentrant' if values[REENTRANT] else 'Non-reentrant' ] )

    #Calculate a common column width for the return value and all arguments, for later field alignment.
    mid_col_min_width = len(values['retval-type'])
    for k in params_dict:
        if params_dict[k]:
            for param in params_dict[k]:
                if len(param[0]) > mid_col_min_width:
                    mid_col_min_width = len(param[0])

    nested_return_table = None
    if values['retval-type'] != 'void':
        retval = [ [ pad_value(values['retval-type'], mid_col_min_width), values['retval-description'] ] ]
        nested_return_table = tabulate(retval, tablefmt="grid")
        table.append( [ RETURN, nested_return_table.replace('$', ' ') ] )
    else:
        table.append( [ RETURN, 'None' ] )

    nested_params_tables = { 'in-params': None, 'out-params' : None, 'inout-params' : None   }
    params_headers = { 'in-params': IN_PARAMS, 'out-params' : OUT_PARAMS, 'inout-params' : IN_OUT_PARAMS }

    for i in [ 'in-params', 'out-params', 'inout-params' ]:
        if len(params_dict[i]) > 0:
            #Pad parameter names to force alignment during tabulation.
            params_dict[i] = [ [ pad_value(param[0], mid_col_min_width), param[1] ] for param in params_dict[i] ]
            nested_params_tables[i] = tabulate(params_dict[i], tablefmt="grid")
            table.append([ params_headers[i], nested_params_tables[i].replace('$', ' ') ])
            #Revert padding.
            params_dict[i] = [ [ param[0].replace('$', ''), param[1] ] for param in params_dict[i] ]
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

    return table_str
