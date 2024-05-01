import ply.yacc as yacc
from lexer import Lexer
import sys
import re



class Parser:

    user_words = {}
        
    
    def __init__(self):
        self.parser = None
        self.tokens = Lexer.tokens
        

    def p_program(self, p):
        """
        program : statements
        """
        p[0] = ""
        
        if p[1]:
            p[0] = "\nstart\n\n" + p[1] + "\n" + "stop\n\n"

        

        # for word, data  in self.user_words.items():
        #     p[0] += f"{word}:\n"
            
        #     code, _, _ = data
            
        #     # for i in range(num_args_needed, 0, -1):
        #     #     p[0] += "pushfp\n"
        #     #     p[0] += f"load -{i}\n"
                
        #     p[0] += f"{code}"
        #     p[0] += "jump\n\n"

    def p_statements(self, p):
        """
        statements : statement
                   | statements statement
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]

            
    def p_statement(self, p):
        """
        statement : instruction
                  | word_definition
        """
        p[0] = p[1]
                
    def p_instruction(self, p):
        """
        instruction : expression_list
                    | control_flow
                    | io_command
        """
        p[0] = p[1]
                
        #print(p[0])

    def p_expression_list(self, p):
        """
        expression_list : expression
                        | expression expression_list
        """
        
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]
            

    def p_expression(self, p):
        """
        expression : value
                   | arithmetic_expression
                   | logical_expression
                   | other_expression
                   | word_call
        """
        p[0] = p[1]
        
    def p_value(self, p):
        """
        value : num
              | str
        """
        p[0] = p[1]
        
        
    def p_num(self, p):
        """
        num : NUMBER
        """
        p[0] = f"pushi {p[1]}\n"
        
    def p_str(self, p):
        """
        str : STRING
        """
        p[0] = f"pushs {p[1]}\n"
        
    def p_arithmetic_expression(self, p):
        """
        arithmetic_expression : expression_list operand
                              | operand
        """
        if len(p) == 3:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]
            
    def p_operand(self, p):
        """
        operand : '+'
                | '-'
                | '*'
                | '/'
                | MOD
        """
        p[0] = ""
        if p[1] == '+': p[0] += "add\n"
        elif p[1] == '-': p[0] += "sub\n"
        elif p[1] == '*': p[0] += "mul\n"
        elif p[1] == '/': p[0] += "div\n"
        elif p[1] == 'MOD': p[0] += "mod\n"

    def p_logical_expression(self, p):
        """
        logical_expression : expression_list '<'
                           | expression_list '>'
                           | expression_list '='
        """
        p[0] = p[1]
        if p[2] == '<': p[0] += "inf\n"
        elif p[2] == '>': p[0] += "sup\n"
        elif p[2] == '=': p[0] += "equal\n"     

    def p_other_expression(self, p):
        """
        other_expression : SWAP
                         | DUP
                         | 2DUP
                         | DROP
                         | RECURSE
                         | DEPTH
        """
        
    
        if p[1] == 'swap':
            p[0] = "swap\n"
            
        elif p[1] == 'dup':
            p[0] = "dup 1\n"
            
        elif p[1] == '2dup': 
            p[0] = "pushsp\nload -1\npushsp\nload -1\n"
            
        elif p[1] == 'drop':     
            p[0] = 'pop 1\n'
            
        elif p[1] == 'recurse':
            
            p[0] = ""
            
        elif p[1] == 'depth':
            p[0] = "depth\n"
        
        
                    


    def p_control_flow(self, p):
        """
        control_flow : if_statement
                     | loop_statement
        """
        p[0] = p[1]

    def p_if_statement(self, p):
        """
        if_statement : instruction IF statements THEN
                     | instruction IF statements ELSE statements THEN
        """
                
        if len(p) == 5:
            p[0] = p[1] + f"jz endif{self.else_labels}\n" + p[3] + f"endif{self.else_labels}:\n"
            self.else_labels += 1

        else:
            p[0] = p[1] + f"jz else{self.else_labels}\n" + p[3] + f"jump endif{self.else_labels}\n" + f"else{self.else_labels}:\n" + p[5] + f"endif{self.else_labels}:\n"
            self.else_labels += 1
            
            
    def p_loop_statement(self, p):
        """
        loop_statement : expression_list DO USER_DEFINED statements LOOP
                       | expression_list DO statements LOOP
        """
        
        
        # 10 0 DO i ."teste" LOOP
        loop_start_label = f"loop{self.while_labels}"
        loop_end_label = f"loopend{self.while_labels}"

        p[0] = p[1]
                        
        if len(p) == 6:
            
            p[0] += "storeg -1\n"
            p[0] += "storeg -2\n"
            
            p[0] += f"{loop_start_label}:\n"

            p[0] += f"pushg -1\n"
            p[0] += f"pushg -2\n"
            p[0] += "inf\n"
            p[0] += f"jz {loop_end_label}\n"
            
            p[0] += f"pushg -1\n"
            p[0] += p[4]
            
            p[0] += f"pushg -1\n"
            p[0] += "pushi 1\n"
            p[0] += "add\n"
            p[0] += "storeg -1\n"
            p[0] += f"jump {loop_start_label}\n"
            p[0] += f"{loop_end_label}:\n"
            
        elif len(p) == 5:
            p[0] += "storeg -1\n"
            p[0] += "storeg -2\n"
            p[0] += f"{loop_start_label}:\n"
            
            p[0] += f"pushg -1\n"
            p[0] += f"pushg -2\n"
            p[0] += "inf\n"
            p[0] += f"jz {loop_end_label}\n"
            p[0] += p[3]
            p[0] += f"pushg -1\n"
            p[0] += "pushi 1\n"
            p[0] += "add\n"
            p[0] += "storeg -1\n"

            p[0] += f"jump {loop_start_label}\n"
            p[0] += f"{loop_end_label}:\n"
        
        self.while_labels += 1
        
        
    def p_word_definition(self, p):
        """
        word_definition : ':' USER_DEFINED statements ';'
        """
        
        self.current_word = p[2]
        code = ''.join(p[3])
        args_needed, args_returned = self.count_stack_operations(code)
        print(f"Argumentos necessários para a word {p[2]}: ", args_needed, args_returned)
        
        self.user_words[p[2]] = (code, args_needed, args_returned)
        p[0] = ""
        
    def count_stack_operations(self, code):
        tokens = code.split()
        stack_effect = self.get_stack_args(tokens)
        return stack_effect

    def get_stack_effect(self, token):
        built_in_effects = {
            'add': (2, 1),
            'sub': (2, 1),
            'mul': (2, 1),
            'div': (2, 1),
            'mod': (2, 1),
            'swap': (2, 2),
            'dup 1': (1, 2),
            'sup': (2, 3),
            'inf': (2, 3),
            'equal': (2, 3),
            'drop': (1, 0),
            'writes': (1, 0),
            'pushs': (0, 1),
            'pushi': (0, 1),
            'writei': (1, 0),
            'jz': (1, 0),
            'storeg': (1, 0),
            'pushg': (0, 1),
        }
        
        if token in built_in_effects:
            return built_in_effects[token]
        
        elif token in self.user_words:
            print("word called: ", token)
            _, arg_needed, args_returned = self.user_words[token]
            print(f"arg_needed: {arg_needed}, args_returned: {args_returned}")
            return arg_needed, args_returned
        
        return 0, 0

        
    def get_stack_args(self, token_sequence):
        needed = 0
        left = 0

        for token in token_sequence:
            args_needed, args_returned = self.get_stack_effect(token)
            if args_needed == 0 and args_returned == 0:
                continue
            if left - args_needed < 0:
                needed += -(left - args_needed)
                left = 0
            else:
                left -= args_needed

            left += args_returned

        return needed, left
    
    
    def p_word_call(self, p):
        """
        word_call : USER_DEFINED
        """
        if p[1] in self.user_words:
            code, _, _ = self.user_words[p[1]]
            p[0] = code
        else:
            print(f"ERROR: Unknown word ({p[1]}) called")
            sys.exit(1)


    def p_io_command(self, p):
        """
        io_command : dot_command
                   | output_command
                   | input_command
        """
        p[0] = p[1]
        
    def p_output_command(self, p):
        """
        output_command : CR
                       | EMIT
                       | TYPE
        """
        if p[1] == 'cr':
            p[0] = "writeln\n"  
        elif p[1] == 'emit':
            p[0] = "writechr\n"
            
    def p_input_commands(self, p):
        """
        input_command : KEY
                      | S str
        """
        if p[1] == 'key':
            p[0] = "CANT BE DONE WITH THIS VM\n"
        else:
            p[0] = f"pushs {p[2]}"
        
    def p_dot_command(self, p):
        """
        dot_command : '.'
                    | '.' str
        """
        if len(p) == 2:
            p[0] = "writei\n"
        else:
            p[0] = p[2]
            p[0] += "writes\n"
    

    def p_error(self, p):   
        print(f"Syntax error at token {p.value} on line {p.lineno}")

    def build(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, debug=True)
        self.else_labels = 0
        self.while_labels = 0
        self.user_words = {}
        self.current_word = None
