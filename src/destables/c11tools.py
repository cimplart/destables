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

from antlr4 import *
from cparser.C11Lexer import C11Lexer
from cparser.C11Parser import C11Parser
from cparser.C11Visitor import C11Visitor

parser = None

def init_parser():

    global parser

    parser = C11Parser(None)

def _decl_from_syntax(syntax):
    decl = syntax.replace('.. code-block::', '')
    decl = decl.replace('\n', ' ')
    decl = decl.strip() + ';'
    return decl

def _parse_declaration(syntax):
    global parser

    c_decl = _decl_from_syntax(syntax)
    if c_decl[-1] != ';':
        c_decl.append(';')

    input_stream = InputStream(c_decl)

    lexer = C11Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser.setInputStream(stream)
    parse_tree = parser.declaration()
    return parse_tree

def extract_original_text(ctx):
    token_source = ctx.start.getTokenSource()
    input_stream = token_source.inputStream
    start, stop  = ctx.start.start, ctx.stop.stop
    return input_stream.getText(start, stop)

class FuncVisitor(C11Visitor):

    def __init__(self) -> None:
        super().__init__()
        self.func_name = None
        self.func_params = []
        self.func_result_type = None
        self._in_params_list = False

    def visitDirectDeclarator(self, ctx: C11Parser.DirectDeclaratorContext):

        if not self._in_params_list:
            if ctx.LeftParen() != None and ctx.RightParen() != None and ctx.parameterTypeList() != None:
                self.func_name = ctx.directDeclarator().Identifier().symbol.text
        else:
            if ctx.Identifier() != None:
                self.func_params.append(ctx.Identifier().symbol.text)
        return super().visitDirectDeclarator(ctx)

    def visitParameterList(self, ctx: C11Parser.ParameterListContext):
        self._in_params_list = True
        return super().visitParameterList(ctx)

    # Visit a parse tree produced by C11Parser#declaration.
    def visitDeclaration(self, ctx:C11Parser.DeclarationContext):
        if ctx.parentCtx is None and len(ctx.children) > 1:
            self.func_result_type = extract_original_text(ctx.declarationSpecifiers())
        return self.visitChildren(ctx)


from antlr4.tree.Trees import Trees

def get_func_info(syntax):
    global parser

    parse_tree = _parse_declaration(syntax)

    #print(Trees.toStringTree(parse_tree, ruleNames=None, recog=parser))

    visitor = FuncVisitor()
    visitor.visit(tree=parse_tree)
    return visitor.func_name, visitor.func_params, visitor.func_result_type


class TypedefVisitor(C11Visitor):

    def __init__(self) -> None:
        super().__init__()
        self.typedef_name = ''
        self.is_typedef = False
        self._skip_identifiers = False

    def visitStorageClassSpecifier(self, ctx: C11Parser.StorageClassSpecifierContext):
        if ctx.Typedef() != None:
            self.is_typedef = True
        return super().visitStorageClassSpecifier(ctx)

    def visitDirectDeclarator(self, ctx: C11Parser.DirectDeclaratorContext):
        if not self._skip_identifiers:
            if ctx.Identifier() is not None:
                self.typedef_name = ctx.Identifier().symbol.text
        return super().visitDirectDeclarator(ctx)

    def visitTypeSpecifier(self, ctx: C11Parser.TypeSpecifierContext):
        if not self._skip_identifiers:
            if ctx.typedefName() != None:
                self.typedef_name = ctx.typedefName().Identifier().symbol.text
        return super().visitTypeSpecifier(ctx)

    #Happens for function type typedefs.
    def visitParameterList(self, ctx: C11Parser.ParameterListContext):
        self._skip_identifiers = True
        return super().defaultResult()


def get_typedef_name(syntax):

    parse_tree = _parse_declaration(syntax)

    visitor = TypedefVisitor()
    visitor.visit(tree=parse_tree)

    if visitor.is_typedef:
        return visitor.typedef_name
    return None

class VarVisitor(C11Visitor):

    def __init__(self) -> None:
        super().__init__()

    def visitDirectDeclarator(self, ctx: C11Parser.DirectDeclaratorContext):
        if ctx.Identifier() is not None:
            self.var_name = ctx.Identifier().symbol.text
        return super().visitDirectDeclarator(ctx)

def get_variable_name(syntax):

    parse_tree = _parse_declaration(syntax)

    visitor = VarVisitor()
    visitor.visit(tree=parse_tree)
    return visitor.var_name
