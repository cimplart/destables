
from pycparser import c_parser, c_ast
import sys

def get_func_params(c_decl):

    parser = c_parser.CParser()

    node = parser.parse(c_decl, filename='')

    if (not isinstance(node, c_ast.FileAST) or not isinstance(node.ext[-1], c_ast.Decl)):
        raise Exception("Not a valid declaration")

    return _seek_func_params(node.ext[-1].type)

def _seek_func_params(decl):

    typ = type(decl)

    if typ == c_ast.FuncDecl:
        result = []
        if decl.args:
            params = [_seek_func_params(param) for param in decl.args.params]
            for param in decl.args.params:
                if param.name is not None:
                    result.append(param.name)

        return result

def get_func_name(c_decl):

    parser = c_parser.CParser()

    node = parser.parse(c_decl, filename='')

    if (not isinstance(node, c_ast.FileAST) or not isinstance(node.ext[-1], c_ast.Decl)):
        raise Exception("Not a valid declaration")

    return _seek_func_name(node.ext[-1].type)

def _seek_func_name(decl):

    if type(decl) == c_ast.FuncDecl:
        return decl.type.declname