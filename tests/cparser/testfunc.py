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
from cparser.C11Visitor import C11Visitor
import c11tools

def _parse(decl: str):
    input_stream = InputStream(decl)
    lexer = C11Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = C11Parser(stream)
    return parser.declaration()

class TestFunctionDeclarations(unittest.TestCase):

    def test_case1(self):
        decl = 'int func(const char *s, size_t len);'
        parse_tree = _parse(decl)

        visitor = c11tools.FuncVisitor()
        visitor.visit(tree=parse_tree)
        self.assertEqual(visitor.func_name, 'func')
        self.assertIn('s', visitor.func_params)
        self.assertIn('len', visitor.func_params)

    def test_case2(self):
        decl = 'void func2(void * p, void (*notification)(enum State));'
        parse_tree = _parse(decl)

        v = c11tools.FuncVisitor()
        v.visit(tree=parse_tree)
        self.assertEqual(v.func_name, 'func2')
        self.assertIn('p', v.func_params)
        self.assertIn('notification', v.func_params)
        self.assertEqual(len(v.func_params), 2)


if __name__ == '__main__':
    unittest.main()
