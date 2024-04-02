import ply.lex as lex

class Lexer:

    reserved = {
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'emit': 'EMIT',
        'cr': 'CR',
        'do': 'DO',
        'loop': 'LOOP',
        'depth': 'DEPTH',
        'dup': 'DUP',
        'mod': 'MOD',
        '.': 'DOT',
        'drop': 'DROP',
        'swap': 'SWAP',
        'space': 'SPACE',
        'spaces': 'SPACES',
        'key': 'KEY'
    }

    tokens = [
        'NUMBER',
        'HEX_NUMBER',
        'FLOAT',
        'STRING',
        'WORD',
        'USER_WORD',
        'COMMENT',
        'ATALHO',
        'COMMA',
        'SEMICOLON',
        'COLON',
        'LPAREN',
        'RPAREN'
    ]+list(reserved.values())

    literals = ['+', '-', '*', '/', '%', '=', '<', '>']

    t_ignore = ' \t\v\f'

    t_NUMBER = r'\d+'
    t_HEX_NUMBER = r'0x[0-9A-Fa-f]+'
    t_FLOAT = r'-?\d+\.\d+([eE][+-]?\d+)?'
    t_STRING = r'"[^"]*"'
    t_ATALHO = r'\d+[\+\-\*\/\%\=\<\>]'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def t_COMMENT(self, t):
        r'\\.*'
        pass

    def t_WORD(self, t):
        r'[a-zA-Z_\.]\w*'
        lower_value = t.value.lower()
        if lower_value not in self.reserved:
            t.type = 'USER_WORD'
        else:
            t.type = self.reserved.get(lower_value, 'WORD')
        return t

    def t_USER_WORD(self, t):
        r'[a-zA-Z_]\w*'
        if t.type != 'WORD':
            t.type = 'USER_WORD'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += 1

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self):
        self.lexer = lex.lex(module=self)



#lexer = Lexer()
#lexer.build()
#
#data = '''
#: FACTORIAL 
#  DUP 1 = 
#  IF 
#    DROP 1 
#  ELSE 
#    DUP 1 - FACTORIAL * 
#  THEN 
#;
#
#: MAIN 
#  CR "Enter a number: " EMIT 
#  KEY DIGIT 
#  CR "The factorial is: " EMIT 
#  FACTORIAL . CR 
#;
#MAIN
#'''
#lexer.lexer.input(data)
#
#for token in lexer.lexer:
#    print(token)
