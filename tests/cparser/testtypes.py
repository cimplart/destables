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

import unittest

import sys
import os

sys.path.append(os.path.dirname(__file__) + os.sep + os.path.join('..', '..', 'src', 'destables'))

from antlr4 import *
from cparser.C11Lexer import C11Lexer
from cparser.C11Parser import C11Parser
import c11tools

def _parse(decl: str):
    input_stream = InputStream(decl)
    lexer = C11Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = C11Parser(stream)
    return parser.declaration()

class TestTypedefDeclarations(unittest.TestCase):

    def test_simple_typedefs(self):

        simple_declarations = [
            'typedef char* char_ptr_t;',
            'typedef int FlagType;',
            'typedef char const *ConstString;',
            'typedef struct MyStruct MyStruct;'
        ]
        typedef_names = [
            'char_ptr_t',
            'FlagType',
            'ConstString',
            'MyStruct'
        ]
        for i in range(len(simple_declarations)):
            decl = simple_declarations[i]
            parse_tree = _parse(decl)
            visitor = c11tools.TypedefVisitor()
            visitor.visit(tree=parse_tree)
            self.assertTrue(visitor.is_typedef)
            self.assertEqual(visitor.typedef_name, typedef_names[i])

    def test_function_ptr_typedefs(self):

        declarations = [
            'typedef (*Notification)(const char buf[], size_t len);'
        ]

        typedef_names = [
            'Notification'
        ]

        for i in range(len(declarations)):
            decl = declarations[i]
            parse_tree = _parse(decl)
            visitor = c11tools.TypedefVisitor()
            visitor.visit(tree=parse_tree)
            self.assertTrue(visitor.is_typedef)
            self.assertEqual(visitor.typedef_name, typedef_names[i])
