# USAGE:
# python3 compiler.py [input_file [output_file]]

import sys
from sly import Lexer, Parser

#################### LEXER ####################

class ÇLexer(Lexer):
    # token definitions
    literals = {';', '+', '-', '*', '/', '%', '(', ')', '{', '}', '[', ']', ',', '='}
    tokens = {'VOID', 'INT', 'MAIN', 'PRINTF', 'IF', 'WHILE', 'STRING', 'NUMBER', 'NAME', 'COMP', 'STDIO'}
    STDIO = '#include <stdio.h>'
    VOID = 'void'
    INT = 'int'
    MAIN = 'main'
    PRINTF = 'printf'
    IF = 'if'
    WHILE = 'while'
    COMP = r'(==|!=|>=|<=|>|<)'
    STRING = r'"[^"]*"'
    NUMBER = r'\d+'
    NAME = r'[a-z]+'

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
        self.while_counter = 1

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', '%'),
        ('left', 'COMP'),
    )

    # error handling method
    def show_error(self, mesg, line=None):
        if line:
            mesg += ' in line ' + str(line)
        print('error:', mesg, file=sys.stderr)
        sys.exit(1)

    # ---------------- program ----------------

    @_('stdio functions main')
    def program(self, p):
        print('\n# symbol_table:', self.symbol_table)
    
    @_('STDIO')
    def stdio(self, p):
        print('LOAD_CONST 0')
        print('LOAD_CONST None')
        print('IMPORT_NAME runtime')
        print('IMPORT_STAR')

    

    # ---------------- Functions ----------------

    @_('functions function')
    def functions(self, p):
        pass

    @_('function')
    def functions(self, p):
        pass
 
    @_('INT function_name "{" statements "}" ')
    def function(self, p):
        print('.end')

    @_('VOID function_name "{" statements "}" ')
    def function(self, p):
        print('.end')

    @_('NAME "(" parameters ")" ')
    def function_name(self, p):
        print('.begin', p.NAME, p.parameters)

    # ---------------- Parameters ---------------------------

    @_('INT NAME parameters_tail')
    def parameters(self, p):
        print()

    @_('')
    def parameters(self, p):
        pass

    @_('"," INT NAME parameters_tail')
    def parameters_tail(self, p):
        print()

    @_('')
    def parameters_tail(self, p):
        pass

    # ---------------- main ----------------

    @_('MAIN "(" ")" "{" statements "}"')
    def main(self, p):
        print('LOAD_CONST None')
        print('RETURN_VALUE')

    # ---------------- statements ----------------

    @_('statements statement')
    def statements(self, p):
        pass

    @_('')
    def statements(self, p):
        pass

    # ---------------- statement ----------------

    @_('printf')
    def statement(self, p):
        pass

    @_('declaration')
    def statement(self, p):
        pass

    @_('attribution')
    def statement(self, p):
        pass

    @_('if_st')
    def statement(self, p):
        pass

    @_('while_st')
    def statement(self, p):
        pass

    @_('decl_array')
    def statement(self, p):
        pass
    
    @_('attr_array')
    def statement(self, p):
        pass

    @_('decl_array2')
    def statement(self, p):
        pass

    @_('call')
    def statement(self, p):
        pass

    # ------------ Call -------------

    @_('NAME')
    def call_name(self, p):
        print('LOAD_NAME', p.NAME)

    @_('call_name "(" arguments ")" ";" ')
    def call(self, p):
        print('LOAD_NAME', p.NAME)
        print('CALL_FUNCTION', p.arguments)
        print('POP_POP')

        

    # ---------------- Arguments ------

    @_('expression "," arguments_tail')
    def arguments(self, p):
        return 1 + p.arguments

    @_('expression')
    def arguments(self, p):
        return 1

    @_('"," expression arguments_tail')
    def arguments_tail(self, p):
        pass

    @_('')
    def arguments_tail(self, p):
        pass

    # -------------- print ----------

    @_('PRINTF "(" STRING "," expression ")" ";"')
    def printf(self, p):
        print('LOAD_GLOBAL', 'print')
        print('LOAD_CONST', p.STRING)
        print('BINARY_MODULO')
        print('CALL_FUNCTION', 1)
        print('POP_TOP')

    # ---------------- declaration ----------------

    @_('INT NAME "=" expression ";"')
    def declaration(self, p):
        if p.NAME in self.symbol_table:
            self.show_error(f"variable {p.NAME} is already declared or cannot be declared")
        print('STORE_NAME', p.NAME)

    # ---------------- attribution ----------------

    @_('NAME "=" expression ";"')
    def attribution(self, p):
        if p.NAME not in self.symbol_table:
            self.show_error(f"variable {p.NAME} not declared")
        print('STORE_NAME', p.NAME)

    # -------------------- declaration of array ---------------

    @_('INT NAME "[" "]" "=" "{" expressions "}" ";" ')
    def decl_array(self, p):
        print('BUILD_LIST:' + str(p.expressions))
        print('STORE_NAME ' + p.NAME)

    @_('expression "," expressions')
    def arguments(self, p):
        return 1 + p.expressions

    # -------------------- declaration of array2 ---------------

    @_('INT NAME "[" expression "]" "=" "{" expressions "}" ";"')
    def decl_array2(self, p):
        print('CALL_FUNCTION 1')
        print('STORE_NAME ' + p.NAME)

    @_('expression "," expressions')
    def expressions(self, p):
        return 1 + p.expressions

    @_('expression')
    def expressions(self, p):
        return 1

    # ------------------- attribution of array ---------------------

    @_('NAME "[" expression "]" "=" expressions  ";"')
    def attr_array(self, p):
        print('ROT_THREE')
        print('STORE_SUBSCR')

    @_('NAME')
    def name_array(self, p):
        print('LOAD_FAST', p.NAME)
        return p.NAME

    # -------------------- if -----------------------

    @_('IF "(" expression COMP expression ")" "{" statements "}"')
    def if_st(self, p):
        print(f'NOT_IF_{self.if_counter}:')
        self.if_counter += 1

    # -------------------- while ------------------------

    @_('WHILE "(" expression COMP expression ")" "{" statements "}"')
    def while_st(self, p):
        print(f'BEGIN_WHILE_{self.while_counter}:')
        self.while_counter += 1
        print(f'END_WHILE_{self.while_counter}:')
        print('LOAD_CONST', 'None')
        print('RETURN_VALUE')

    # --------------------- expression ----------------
    

    @_('expression "+" term',
       'expression "-" term')
    def expression(self, p):
        if p[2] == '+':
            print('BINARY_ADD')
        elif p[2] == '-':
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
        print('BINARY_FLOOR_DIVIDE')

    @_('term "%" factor')
    def term(self, p):
        print('BINARY_MODULO')

    @_('expression COMP expression')
    def expression(self, p):
        print(f'COMP_OP: {p.COMP}')

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

    @_('name_array "[" expression "]" ')
    def factor(self, p):
        print('BINARY_SUBSCR')

    @_('NAME')
    def factor(self, p):
        if p.NAME not in self.symbol_table:
            self.show_error(f" unknown variable '{p.NAME}' ", p.lineno)
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

