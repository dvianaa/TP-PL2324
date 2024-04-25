import ply.lex as lex
import sys

class Lexer:

    reserved = {
        'mod' : 'MOD',
        'key' : 'KEY',
        'cr'  : 'CR',
        'emit': 'EMIT',
        'char': 'CHAR',
        'if'  : 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'do'  : 'DO',
        'loop': 'LOOP',
        'dup' : 'DUP',
        'swap': 'SWAP',
    }
    
    literals = "+-*/.;:<>="
    
    tokens = [
        'NUMBER',
        'WORD',
        'COMMENT',
    ]+list(reserved.values())

        
    t_ignore = r' \t'
    
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_WORD(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value.lower() in self.reserved:
            t.type = self.reserved[t.value]
        else:
            t.type = 'WORD'
        return t

    def t_COMMENT(self, t):
        r"//.*"
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += 1

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        sys.exit(1)

    def build(self):
        self.lexer = lex.lex(module=self)



# lexer = Lexer()
# lexer.build()

# data = '''
# 10 0 DO
#     I . CR
# LOOP
# '''
# lexer.lexer.input(data)

# for token in lexer.lexer:
#    print(token)
