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
import re

def hidable(layout, key):
    return sg.pin(sg.Column(layout, key=key))

def show_inner_table(initial_values, header, required_cols, col_width):

    result = initial_values

    MAX_ROWS = 1 + 16
    MAX_COL = len(header)

    inner_layout = [ [ sg.Input(pad=(1,1), justification='left', key=str(i)+','+str(j), enable_events=True, size=(col_width[j], 1))
                      for j in range(MAX_COL) ] for i in range(MAX_ROWS) ]

    column_layout = [ [ hidable([ inner_layout[row] ], key=row) ] for row in range(MAX_ROWS) ]

    layout = [ [ sg.Col(column_layout, scrollable=True) ],
               [ sg.Push(), sg.Ok(size=(15, 1)), sg.Cancel(size=(15, 1)) ] ]

    window = sg.Window('Add feature elements', layout, finalize=True)

    #Fill header row.
    for col in range(MAX_COL):
        window['0,'+str(col)].update(background_color='cyan')   #doesn't work :(
        window['0,'+str(col)].update(value=header[col], disabled=True)

    for row in range(len(initial_values)):
        for col in range(MAX_COL):
            window[str(row+1)+','+str(col)].update(value=initial_values[row][col])

    for row in range(1, MAX_ROWS):
        if row > len(initial_values)+1:
            window[row].update(visible=False)
        for col in range(MAX_COL):
            window[str(row)+','+str(col)].bind("<Return>", "_RETURN")
    last_visible_row = len(initial_values) + 1
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
            for row in range(1, last_visible_row+1):
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
