#!/usr/bin/env python3

# Ç version 2.0

# USAGE:
# python3 compiler.py [input_file [output_file]]

import sys
from sly import Lexer, Parser

#################### LEXER ####################

class ÇLexer(Lexer):
    
    # token definitions
    literals = {';', '+', '-', '*', '/', '(', ')', '{', '}', ',', '=', '%', '[', ']'}
    tokens = {STDIO, INT, MAIN, PRINTF, IF, WHILE, STRING, NUMBER, NAME, COMP, VOID}
    VOID = 'void'
    STDIO   = '#include <stdio.h>'
    INT     = 'int'
    MAIN    = 'main'
    PRINTF  = 'printf'
    IF      = 'if'
    COMP    = r'(==|!=|>=|<=|>|<)'
    WHILE = 'while'

    STRING  = r'"[^"]*"'
    NUMBER  = r'\d+'
    NAME    = r'[a-z]+'


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
        self.if_stack = []
        self.while_stack = []
        self.while_counter = []
        self.if_counter = 1
        self.while_counter = 1
        

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
        
    @_('NAME "(" parameters ")"')
    def function_name(self, p):
        print('.begin', p.NAME, p.parameters)
        # Adicionar nomes dos parâmetros na tabela de símbolos
        for param in p.parameters.split(' '):
            self.symbol_table.append(param)
            
            
    @_("VOID function_name '{' statements '}'")
    def function(self,p):
        print('LOAD CONST None')
        print('RETURN_VALUE')
        print('.end')
        self.symbol_table.clear()


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
        print('LOAD_CONST None')
        print('RETURN_VALUE')

    # ---------------- statements ----------------

    @_('statement statements')
    def statements(self, p):
        pass

    @_('')
    def statements(self, p):
        pass

    # ---------------- statement ----------------

    @_('printf')
    def statement(self, p):
        print()

    @_('declaration')
    def statement(self, p):
        print()

    @_('attribution')
    def statement(self, p):
        print()

    @_('if_st')
    def statement(self, p):
        print()
        
    @_('while_st')
    def statement(self,p):
        print()
    
    @_('call')
    def statement(self,p):
        print()
        
    # ---------------- call ----------------
    @_('NAME')
    def call_name(self,p):
        print('LOAD_NAME',p.NAME)
    
    @_('call_name "(" arguments ")" ";"')
    def call(self,p):
        print('CALL_FUNCTION',p.arguments)
        print('POP_TOP') 
        
    # ---------------- arguments ----------------
    @_('expression "," arguments')
    def arguments(self,p):
        return 1 + p.arguments

    @_('expression')
    def arguments(self,p):
        return 1
    
    @_('')
    def arguments(self,p):
        return 0
        
    # ---------------- printf ----------------

    @_('STRING')
    def printf_format(self, p):
        print('LOAD_GLOBAL', 'print')
        print('LOAD_CONST', p.STRING)

    @_('PRINTF "(" printf_format "," expression ")" ";"')
    def printf(self, p):
        print('BINARY_MODULO')
        print('CALL_FUNCTION', 1)
        print('POP_TOP')

    # ---------------- declaration ----------------

    @_('INT NAME "=" expression ";"')
    def declaration(self, p):
        if p.NAME in self.symbol_table:
            self.show_error(f"cannot redeclare variable '{p.NAME}'")
        else:
            self.symbol_table.append(p.NAME)
            print('STORE_FAST', p.NAME)
    
    
    

   # ---------------- if ----------------
   
   
   #@_('IF "(" expression COMP expression ")" "{" statements "}"')
    #def if_st(self, p):
    #    pass

    @_('expression COMP expression')
    def if_comparison(self,p):
        print('COMPARE_OP',p.COMP)
        #label = 'NOT_IF' + str
        print('POP_JUMP_IF_FALSE', f"{self.if_counter}")
        #print('POP_JUMP_IF_FALSE',label)
        self.if_stack.append(self.if_counter)
        self.if_counter += 1
        
    @_('IF "(" if_comparison ")" "{" statements "}"')
    def if_st(self,p):
        print(f"NOT_IF_{self.if_stack.pop()}")

    # ---------------- while ----------------
    @_('WHILE')
    def while_begin(self,p):
        print(f"BEGIN_WHILE_{self.while_counter}")
    
    @_('expression COMP expression')
    def while_comparison(self,p):
        pass
    
    @_('WHILE "(" expression ")" "{" statements "}"')
    def while_st(self, p):
        print('SETUP_LOOP')
        print(f'NOT_IF{self.if_counter}:')
        self.if_stack.append(f'NOT_IF{self.if_counter}')
        self.if_counter += 1
        pass

    # ---------------- attribution ----------------

    @_('NAME "=" expression ";"')
    def attribution(self, p):
        if p.NAME not in self.symbol_table:
            self.show_error(f"variable '{p.NAME}' not declared") 
        print('STORE_FAST', p.NAME)

    # ---------------- expression ----------------

    @_('expression "+" term')
    def expression(self, p):
        print('BINARY_ADD')

    @_('expression "-" term')
    def expression(self, p):
        print('BINARY_SUBTRACT')

    @_('term')
    def expression(self, p):
        pass

    # ---------------- term ----------------

    @_('term "*" factor')
    def term(self, p):
        print('BINARY_MULTIPLY')

    @_('term "/" factor')
    def term(self, p):
        print('BINARY__DIVIDE')

    @_('term "%" factor')
    def term(self, p):
        print('BINARY__MODULO')

    @_('factor')
    def term(self, p):
        pass

    # ---------------- factor ----------------

    @_('NUMBER')
    def factor(self, p):
        print('LOAD_CONST', p.NUMBER)

    @_('"(" expression ")"')
    def factor(self, p):
        pass

    @_('NAME')
    def factor(self, p):
        if p.NAME not in self.symbol_table:
            self.show_error(f"unknown variable '{p.NAME}'", p.lineno)
        print('LOAD_FAST', p.NAME)


            
#################### MAIN ####################

lexer = ÇLexer()
parser = ÇParser()

if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')

if len(sys.argv) > 2:
    sys.stdout = open(sys.argv[2], 'w')

text = sys.stdin.read()
parser.parse(lexer.tokenize(text))
