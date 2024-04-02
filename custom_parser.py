import ply.yacc as yacc
from custom_lexer import Lexer


class Parser:

    tokens = Lexer.tokens

    def __init__(self):
        self.parser = None
        self.vm_commands = []


    def p_program(self, p):
        """
        program : statements
        """
        p[0] = ''.join(p[1])

    def p_statements(self, p):
        """
        statements : statement
                   | statements statement
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """
        statement : expression
                  | control_flow
                  | definition
                  | io_command
                  | function_call
        """
        p[0] = p[1]

    def p_expression_list(self, p):
        """
        expression_list : expression
                        | expression_list expression
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_expression(self, p):
        """
        expression : NUMBER
                   | expression expression '+'
                   | expression expression '-'
                   | expression expression '*'
                   | expression expression '/'
                   | expression expression '%'
                   | expression expression '<'
                   | expression expression '>'
                   | expression expression '='
        """
        if len(p) == 2:
            p[0] = f"pushi {p[1]}\n"
        else:
            p[0] = p[1] + p[2]
            if p[3] == '+': p[0] += "ADD\n"
            elif p[3] == '-': p[0] += "SUB\n"
            elif p[3] == '*': p[0] += "MUL\n"
            elif p[3] == '/': p[0] += "DIV\n"
            elif p[3] == 'MOD': p[0] += "MOD\n"
            elif p[3] == '<': p[0] += "INF\n"
            elif p[3] == '>': p[0] += "SUP\n"
            elif p[3] == '=': p[0] += "EQUAL\n"

    #def p_shortcut(self, p):

    def p_control_flow(self, p):
        """
        control_flow : if_statement
                     | loop_statement
        """
        p[0] = p[1]

    def p_if_statement(self, p):
        """
        if_statement : expression IF statements THEN
                     | expression IF statements ELSE statements THEN
        """
        if len(p) == 5:
            p[0] = f"{p[1]} JZ ELSE{len(self.vm_commands)}\n"   
            p[0] += ''.join(p[3])
            p[0] += f"JUMP ENDIF{len(self.vm_commands)}:\n"
            p[0] += f"ELSE{len(self.vm_commands)}:\n" 
            p[0] += ''.join(p[5])
            p[0] += f"ENDIF{len(self.vm_commands)}:\n"
        else:
            p[0] = f"{p[1]} JZ ENDIF{len(self.vm_commands)}\n"
            p[0] += ''.join(p[3])
            p[0] += f"ENDIF{len(self.vm_commands)}:\n"

    def p_loop_statement(self, p):
        """
        loop_statement : expression DO statements LOOP
        """
        p[0] = f"LOOP{len(self.vm_commands)}:\n"
        p[0] += ''.join(p[4])
        p[0] += f"{p[1]} JNZ LOOP{len(self.vm_commands)}\n"

    def p_definition(self, p):
        """
        definition : ':' WORD statements ';'
        """
        p[0] = f"{p[2]}:\n"
        p[0] += ''.join(p[3])
        p[0] += f"RETURN\n"

    def p_function_call(self, p):
        """
        function_call : WORD
                      | WORD expression_list
        """
        if len(p) == 2:
            p[0] = f"{p[1]}\n"
            p[0] += "CALL\n"
        else:
            p[0] = ''.join(p[2]) + f"{p[1]}\n"

    def p_io_command(self, p):
        """
        io_command : EMIT
                   | KEY
                   | SPACE
                   | SPACES
                   | CR
                   | DOT
        """
        if p[1] == '.':   
            p[0] = 'WRITEI\n' 
        elif p[1] == 'SPACE':
            p[0] = 'PUSHS " "\nWRITES\n'
        elif p[1] == 'SPACES':
            p[0] = 'PUSHS "  "\nWRITES\n'
        elif p[1] == 'CR':
            p[0] = "WRITELN\n"
        elif p[1] == 'EMIT':
            p[0] == "EMIT\n" # o que fazer?? deveria imprimir o ascii correspondente ao char no topo da stack
        elif p[1] == 'KEY':
            p[0] == "KEY\n" # ??? devia inputar 1 char no keyboard mas na vm só existe comando para stirng completa??

    def p_error(self, p):
        print(f"Syntax error at token {p.value} on line {p.lineno}")

    def build(self):
        self.fp = dict()
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)
