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

from typewin import *
from funcwin import *
import PySimpleGUI as sg

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
            show_function_table()

    window.close()

if __name__ == "__main__":
    main()
