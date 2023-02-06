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

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typewin import *
from funcwin import *
from varwin import *
import PySimpleGUI as sg
from c11tools import init_parser

TABLE_DIRECTIVE = 'Add .. table:: directive'
INDENT_SIZE = "Indentation"

def main():

    init_parser()

    layout = [ [ sg.Checkbox(text=TABLE_DIRECTIVE, key=TABLE_DIRECTIVE, default=True) ],
               [ sg.Text(INDENT_SIZE, k=INDENT_SIZE+'-label'), sg.Push(),
                 sg.Slider(orientation ='horizontal', key=INDENT_SIZE, range=(0,4), default_value=4, size=(15, 20)) ],
              [ sg.HorizontalSeparator() ],
              [ sg.Button('Type table', key='type', size = (30, 2)) ],
              [ sg.Button('Function table', key='function', size = (30, 2)) ],
              [ sg.Button('Variables table', key='variables', size = (30, 2)) ],
#              [ sg.Button('Macro constants table', key='macro-constants', size = (30, 2)) ],
#              [ sg.Button('Macro function table', key='macro-function', size = (30, 2)) ],
              [ sg.HorizontalSeparator() ],
              [ sg.Button('Exit', size = (30, 3))] ]

    window = sg.Window('SW Design Tables Tool', layout)

    while True:
        event, values = window.read()
        print(event, values)
        indent_size = int(values[INDENT_SIZE])
        add_table_dir = values[TABLE_DIRECTIVE]
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'type':
            show_type_table(indent_size, add_table_dir)
        elif event == 'function':
            show_function_table(indent_size, add_table_dir)
        elif event == 'variables':
            show_variable_table(indent_size, add_table_dir)

    window.close()

if __name__ == "__main__":
    main()
