from sly import Lexer, Parser

#################### LEXER ####################

class CalcLexer(Lexer):
    
    # token definitions
    tokens = { PLUS, MINUS, TIMES, OVER, OPEN, CLOSE, NUMBER }
    PLUS   = r'\+'
    MINUS  = r'-'
    TIMES  = r'\*'
    OVER   = r'/'
    OPEN   = r'\('
    CLOSE  = r'\)'
    NUMBER = r'\d+'

    # ignored characters and patterns
    ignore = ' \t'
    ignore_newline = r'\n+'

    # extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # error handling method
    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1

#################### PARSER ####################

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    # ---------------- start ----------------

    @_('expression')
    def start(self, p):
        print('LOAD_CONST None')
        print('RETURN_VALUE')

    # ---------------- expression ----------------

    @_('expression PLUS term')
    def expression(self, p):
        print('BINARY_ADD')

    @_('expression MINUS term')
    def expression(self, p):
        print('BINARY_SUBTRACT')

    @_('term')
    def expression(self, p):
        pass

    # ---------------- term ----------------

    @_('term TIMES factor')
    def term(self, p):
        print('BINARY_MULTIPLY')

    @_('term OVER factor')
    def term(self, p):
        print('BINARY_TRUE_DIVIDE')

    @_('factor')
    def term(self, p):
        pass

    # ---------------- factor ----------------

    @_('NUMBER')
    def factor(self, p):
        print('LOAD_CONST', p.NUMBER)

    @_('OPEN expression CLOSE')
    def factor(self, p):
        pass

#################### MAIN ####################

lexer = CalcLexer()
parser = CalcParser()

while True:
    try:
        text = input('calc > ')
    except EOFError:
        break
    if text:
        parser.parse(lexer.tokenize(text))
