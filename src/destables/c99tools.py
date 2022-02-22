
import os
from lark import Lark
from lark.visitors import Visitor
from lark import Token, Tree

parser = None

def init_parser():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    grammar_file_path = os.path.join(dir_path, "c99.lark")
    f = open(grammar_file_path)

    global parser

    parser = Lark(f.read(), debug=True)

def _decl_from_syntax(syntax):
    decl = syntax.replace('.. code-block::', '')
    decl = decl.replace('\n', ' ')
    decl = decl.strip() + ';'
    return decl

class FuncVisitor(Visitor):

    def __init__(self) -> None:
        super().__init__()
        self.f_name = ''
        self.f_params = []

    def function_declarator(self, tree):
        assert len(tree.children) == 2
        assert tree.children[0].data == 'direct_declarator'
        assert isinstance(tree.children[0].children[0], Token)
        assert tree.children[0].children[0].type == 'IDENTIFIER'
        assert tree.children[1].data == 'parameter_type_list'
        self.f_name = tree.children[0].children[0].value

    def _print_tree(self, tree, indent):
        for c in tree.children:
            if isinstance(c, Token):
                print(' ' * indent, 'Token[', c.type, ']: ', c.value)
            else:
                print(' ' * indent, 'Tree[', c.data, ']')
                self._print_tree(c, indent * 2)

    def _get_identifier(self, tree):
        for c in tree.children:
            if isinstance(c, Token) and c.type == 'IDENTIFIER':
                return c.value
            else:
                ident = self._get_identifier(c)
                if ident != None:
                    return ident
        return None

    def parameter_declaration(self, tree):
        #self._print_tree(tree, 3)
        assert tree.children[0].data == 'declaration_specifiers'    #not used
        if tree.children[1].data == 'declarator':
            param = self._get_identifier(tree.children[1])
            self.f_params.append(param)
        elif tree.children[1].data == 'abstract_declarator':    #not allowed in syntax
            raise Exception("abstract declarators are not allowed in syntax input")

#    def __default__(self, tree):
#        print(tree.data)

def get_func_info(syntax):

    c_decl = _decl_from_syntax(syntax)

    parse_tree = parser.parse(c_decl + '\n')

    visitor = FuncVisitor()
    visitor.visit_topdown(tree=parse_tree)
    return visitor.f_name, visitor.f_params

