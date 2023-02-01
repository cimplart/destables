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

import tabulate
import re

def _find_header_rownum(header, tab_lines):
    header_row_num = None
    for l in tab_lines:
        if header in l:
            header_row_num = tab_lines.index(l)
            break
    if header_row_num is None:
        raise Exception('Inconsistent arguments: nested table header not found in table')
    return header_row_num

def _replace(s, at, line):
    return line[:at] + s + line[at+len(s):]

def merge_nested_tables(nested_dict, table_str):

    tab_lines = table_str.split('\n')
    for nested_header in nested_dict:
        nested_table = nested_dict[nested_header]
        nested_tab_lines = nested_table.split('\n')

        header_row_num = _find_header_rownum(nested_header, tab_lines)
        bottom_frame_num = header_row_num + 1
        while tab_lines[bottom_frame_num][0] == '|':
            bottom_frame_num += 1

        nested_tab_pos = tab_lines[header_row_num].find(nested_tab_lines[0])
        if nested_tab_pos < 0:
            raise Exception('Inconsistent arguments: 1st line of nested table not found in table')
        nested_tab_lines[0] = '-' + nested_tab_lines[0][1:-1] + '-'
        # top frame row
        tab_lines[header_row_num-1] = _replace(nested_tab_lines[0], nested_tab_pos, tab_lines[header_row_num-1])
        # bottom frame row
        tab_lines[bottom_frame_num] = _replace(nested_tab_lines[0], nested_tab_pos, tab_lines[bottom_frame_num])
        # copy nested table header to next row
        tab_lines[header_row_num+1] = _replace(nested_header, tab_lines[header_row_num].find(nested_header), tab_lines[header_row_num+1])
        # perform the merge
        for row in range(header_row_num, bottom_frame_num):
            tab_lines[row] = tab_lines[row].replace('| +', '+--')
            # For example '+     |' gets replaced with '------+'
            def repl_fun(matchobj):
                return '-' + '-' * len(matchobj.group(1)) + '+'
            tab_lines[row] = re.sub(r'\+([ ]+)\|', repl_fun, tab_lines[row])
            for i in range(len(tab_lines[header_row_num-1])):
                if tab_lines[row][i] == '|' and tab_lines[header_row_num-1][i] != '+':
                    tab_lines[row] = _replace(' ', i, tab_lines[row])
        # remove lower reduntant frame row
        del tab_lines[bottom_frame_num-1]
        # remove upper reduntant frame row
        del tab_lines[header_row_num]

        result = ''
        for l in tab_lines:
            result += l + '\n'
        return result

def _decorate_table(table_str, indent_size, add_table_dir):

    decorated_str = '.. table::\n\n' if add_table_dir else ''

    lines = table_str.split('\n')
    for l in lines:
        decorated_str += indent_size * ' ' + l + '\n'

    return decorated_str
