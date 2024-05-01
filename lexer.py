import ply.lex as lex
import sys

class Lexer:

    reserved = {
        'mod' : 'MOD',
        'drop': 'DROP',
        'dup' : 'DUP',
        '2dup': '2DUP',
        'swap': 'SWAP',
        'cr'  : 'CR',
        'emit': 'EMIT',
        'key' : 'KEY',
        'if'  : 'IF',
        'else': 'ELSE',
        'then': 'THEN',
        'do'  : 'DO',
        'loop': 'LOOP',
        'char': 'CHAR',
        'accept': 'ACCEPT',
        'query' : 'QUERY',
        's'     : 'S',
        'type'  : 'TYPE',
        'recurse': 'RECURSE',
        'depth' : 'DEPTH',
        
    }
    
    literals = "+-*/;:<>=."
    
    tokens = [
        'NUMBER',
        'STRING',
        'USER_DEFINED',
        'COMMENT',
    ]+list(reserved.values())

        
    t_ignore = r' '
    
    def t_COMMENT(self, t):
        r'\(.*\)'
        pass    
    
    def t_STRING(self, t):
        r'"[^"]*"'
        return t
    
    
    def t_NUMBER(self, t):
        r'\b\d+\b'
        t.value = int(t.value)
        return t
    
    def t_USER_DEFINED(self, t):
        r'[a-zA-Z_0-9][a-zA-Z0-9_]*'
        if t.value.lower() in self.reserved:
            t.type = self.reserved[t.value.lower()]
        else:
            t.type = 'USER_DEFINED'
        return t

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
# : EGGSIZE
# : somatorio 0 swap 1 do i + loop ;
# 11 somatorio .
# ''' 
# lexer.lexer.input(data)

# for token in lexer.lexer:
#    print(token)
