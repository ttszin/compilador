#!/usr/bin/env python3

# Ç version 2.0

# USAGE:
# python3 compiler.py [input_file [output_file]]

import sys
from sly import Lexer, Parser

#################### LEXER ####################

class ÇLexer(Lexer):
    
    # token definitions
    # token definitions
    literals = {';', '+', '-', '*', '/', '(', ')', '{', '}', ',', '=', '%', '[', ']'}
    tokens = {STDIO, INT, MAIN, PRINTF, IF, STRING, NUMBER, COMP, NAME}
    STDIO = '#include <stdio.h>'
    INT = 'int'
    MAIN = 'main'
    PRINTF = 'printf'
    IF = 'if'
    COMP = r'(==|!=|>=|<=|>|<)'
    STRING = r'"[^"]*"'
    NUMBER = r'\d+'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'






    # ignored characters and patterns
    ignore = r' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'//[^\n]*'

    # extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # error handling method
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' in line {self.lineno}")
        self.index += 1

#################### PARSER ####################

class ÇParser(Parser):
    tokens = ÇLexer.tokens
    
    def __init__(self):
        self.symbol_table = []
        self.if_counter = 1

    # error handling method
    def show_error(self, msg, line=None):
        if line:
            msg += ' in line ' + str(line)
            print('error:', msg, file=sys.stderr)
        sys.exit(1)
        
    # ---------------- program ----------------

    @_('STDIO functions main')
    def program(self, p):
        print('\n# symbol_table:', self.symbol_table)

    # ---------------- functions ----------------
    @_('function functions')
    def functions(self, p):
        pass
            
    @_('')
    def functions(self,p):
        pass

    @_('NAME "(" parameters ")" "{" statements "}"')
    def function(self, p):
        print(f'.begin {p.NAME} {p.parameters}')
        for param in p.parameters.split(' '):
            self.symbol_table.append(param)
        pass

    # ---------------- parameters ----------------
    @_('INT NAME')
    def parameters(self,p):
        return p.NAME
        
    @_('')
    def parameters(self,p):
        return ''
        
    @_('INT NAME "," parameters')
    def parameters(self,p):
        return p.NAME + ' ' + p.parameters

    # ---------------- main ----------------

    @_('INT MAIN "(" ")" "{" statements "}"')
    def main(self, p):
        print('LOAD_CONST 2')
        print('STORE_NAME a')

    # ---------------- statements ----------------

    @_('statement statements')
    def statements(self, p):
        pass

    @_('')
    def statements(self, p):
        pass

    # ---------------- statement ----------------

    @_('if_st')
    def statement(self, p):
        pass

    @_('declaration')
    def statement(self, p):
        pass

    @_('printf')
    def statement(self, p):
        pass

    # ---------------- if ----------------

    @_('IF "(" expression COMP expression ")" "{" statements "}"')
    def if_st(self, p):
        print(f'LOAD_NAME {p.expression0}')
        print(f'LOAD_CONST {p.expression1}')
        print(f'COMPARE_OP {p.COMP}')
        print(f'POP_JUMP_IF_FALSE NOT_IF_{self.if_counter}')
        pass

    # ---------------- declaration ----------------

    @_('INT NAME "=" expression ";"')
    def declaration(self, p):
        print(f'STORE_NAME {p.NAME}')
        pass

    # ---------------- printf ----------------

    @_('PRINTF "(" STRING "," expression ")" ";"')
    def printf(self, p):
        print('LOAD_GLOBAL print')
        print(f'LOAD_CONST {p.STRING}')
        print(f'LOAD_NAME {p.expression}')
        print('BINARY_MODULO')
        print('CALL_FUNCTION 1')
        print('POP_TOP')
        pass

    # ---------------- expression ----------------

    @_('NUMBER')
    def expression(self, p):
        return p.NUMBER

    @_('NAME')
    def expression(self, p):
        return p.NAME

#################### MAIN ####################

lexer = ÇLexer()
parser = ÇParser()

text = """#include <stdio.h>

int main() {
    int a = 2;
    if (a < 3) {
        a = 4;
    }
    printf("%d\n", a);
}"""

parser.parse(lexer.tokenize(text))
