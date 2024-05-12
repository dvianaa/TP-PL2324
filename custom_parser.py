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
                  | variable_definition
        """
        
        if p.slice[1].type == 'word_definition':
            p[0] = p[1]
            self.current_word = None
        p[0] = p[1]
        
    def p_variable_definition(self, p):
        """
        variable_definition : VARIABLE USER_DEFINED
        """
        
        if not self.variables_table.check_variable(p[2]):
            print(f"ERROR: Variable name ({p[2]}) already binded to a memory address")
            sys.exit(1)
                
                
        elif p[2] in self.user_words:
            print(f"ERROR: Variable name ({p[2]}) already in use by a user word")
            sys.exit(1)
                
        else:
            self.variables_table.add_symbol(p[2])
                
            p[0] = f"alloc 1\npushi 0\nstore 0\n"
                
    def p_instruction(self, p):
        """
        instruction : expression_list
                    | control_flow
                    | io_command
        """

        p[0] = p[1]
    

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
                   | arithmetic_logical_expression
                   | other_expression
                   | word_call
                   | variable_command
        """
        p[0] = p[1]
        
    def p_variable_command(self, p):
        """
        variable_command : assignment
                         | reference
        """

        p[0] = p[1]
    
        
    def p_reference(self, p):
        """
        reference : USER_DEFINED '@'
        """
            
        if self.variables_table.check_variable(p[1]):
            print(f"ERROR: Variable name ({p[1]}) not declared")
            sys.exit(1)
            
        else:
            p[0] = f"pushst {self.variables_table.get_symbol_index(p[1])}\nload 0\n"
        
    def p_assignment(self, p):
        """
        assignment : USER_DEFINED '!'
        """
        
        
        if self.variables_table.check_variable(p[1]):
            print(f"ERROR: Variable name ({p[1]}) not declared")
            sys.exit(1)
            
        else:
            p[0] = f"storel -1\npushst {self.variables_table.get_symbol_index(p[1])}\npushl -1\nstore 0\n"
        
    def p_value(self, p):
        """
        value : num
              | str
        """
        p[0] = p[1]
        
        
    def p_num(self, p):
        """
        num : NUM
        """
        p[0] = f"pushi {p[1]}\n"
        
    def p_str(self, p):
        """
        str : STRING
        """
        p[0] = f"pushs {p[1]}\n"
        
    def p_arithmetic_logical_expression(self, p):
        """
        arithmetic_logical_expression : expression_list operand
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
                | '<'
                | '>'
                | '='
                | MOD
                
        """
        p[0] = ""
        if p[1] == '+': p[0] += "add\n"
        elif p[1] == '-': p[0] += "sub\n"
        elif p[1] == '*': p[0] += "mul\n"
        elif p[1] == '/': p[0] += "div\n"
        elif p[1] == 'mod': p[0] += "mod\n"
        elif p[1] == '<': p[0] += "inf\n"
        elif p[1] == '>': p[0] += "sup\n"
        elif p[1] == '=': p[0] += "equal\n"   

    def p_other_expression(self, p):
        """
        other_expression : SWAP
                         | DUP
                         | 2DUP
                         | DROP
        """
        
    
        if p[1] == 'swap':
            p[0] = "swap\n"
            
        elif p[1] == 'dup':
            p[0] = "dup 1\n"
            
        elif p[1] == '2dup': 
            p[0] = "pushsp\nload -1\npushsp\nload -1\n"
            
        elif p[1] == 'drop':     
            p[0] = 'pop 1\n'
        
        
    def p_control_flow(self, p):
        """
        control_flow : if_statement
                     | loop_statement
        """
        if p[1] == 'loop_statement':
            p[0] = p[1]
        else:
            p[0] = p[1]

    def p_if_statement(self, p):
        """
        if_statement : instruction IF statements THEN
                     | instruction IF statements ELSE statements THEN
        """
                
        if len(p) == 5:
            p[0] = p[1] + f"jz endif<ELSE_COUNTER>\n" + p[3] + f"endif<ELSE_COUNTER>:\n"

        else:
            p[0] = p[1] + f"jz else<ELSE_COUNTER>\n" + p[3] + f"jump endif<ELSE_COUNTER>\n" + f"else<ELSE_COUNTER>:\n" + p[5] + f"endif<ELSE_COUNTER>:\n"
            
        if self.current_word is None:
            p[0] = self.replace_else_labels(p[0], self.else_labels)
            
    def replace_else_labels(self, code, else_counter):
        """
        Replace placeholders for conditional labels with actual else counter value
        """
        oldcode = code
        newcode = re.sub(r'<ELSE_COUNTER>', str(else_counter), code)
        if newcode != oldcode:
            self.else_labels += 1
        return newcode
    
    def restore_else_placeholders(self, code):
        """
        Replace else counter value back to the placeholders for future iterations
        """

        code = re.sub(r'else(\d+)', r'else<ELSE_COUNTER>', code)
        code = re.sub(r'endif(\d+)', r'endif<ELSE_COUNTER>', code)
        return code
            
            
    def p_loop_statement(self, p):
        """
        loop_statement : expression_list DO statements LOOP
                       | expression_list DO USER_DEFINED statements LOOP
        """
        
        
        current_heap = self.variables_table.index_counter

        p[0] = p[1]
                        
        if len(p) == 6:
            loop_start_label = f"loop<LOOP_COUNTER>"
            loop_end_label = f"loopend<LOOP_COUNTER>"
            
            p[0] += "storeg -1\n"
            p[0] += "storeg -2\n"
            p[0] += "alloc 2\n"
            p[0] += "pushg -1\n"
            p[0] += "store 0\n"
            p[0] += f"pushst {current_heap}\n"
            p[0] += "pushg -2\n"
            p[0] += "store 1\n"
            
            p[0] += f"{loop_start_label}:\n"
            
            
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 0\n"
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 1\n"
            p[0] += "inf\n"
            p[0] += f"jz {loop_end_label}\n"
            
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 0\n"
            p[0] += p[4]
            
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 0\n"
            p[0] += "pushi 1\n"
            p[0] += "add\n"
            p[0] += "store 0\n"
            p[0] += f"jump {loop_start_label}\n"
            p[0] += f"{loop_end_label}:\n"
            p[0] += "popst\n"
            
        elif len(p) == 5:
            loop_start_label = f"loop<LOOP_COUNTER>"
            loop_end_label = f"loopend<LOOP_COUNTER>"
            
            p[0] += "storeg -1\n"
            p[0] += "storeg -2\n"
            p[0] += "alloc 2\n"
            p[0] += "pushg -1\n"
            p[0] += "store 0\n"
            p[0] += f"pushst {current_heap}\n"
            p[0] += "pushg -2\n"
            p[0] += "store 1\n"
            p[0] += f"{loop_start_label}:\n"
        
            
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 0\n"
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 1\n"
            p[0] += "inf\n"
            p[0] += f"jz {loop_end_label}\n"
            p[0] += p[3]
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"pushst {current_heap}\n"
            p[0] += f"load 0\n"
            p[0] += "pushi 1\n"
            p[0] += "add\n"
            p[0] += "store 0\n"

            p[0] += f"jump {loop_start_label}\n"
            p[0] += f"{loop_end_label}:\n"
            p[0] += "popst\n"
            
        if self.current_word is None:
            p[0] = self.replace_loop_labels(p[0], self.while_labels)
            
    def replace_loop_labels(self, code, loop_counter):
        """
        Replace placeholders for loop labels with actual loop counter value
        """
        old_code = code
        newcode = re.sub(r'<LOOP_COUNTER>', str(loop_counter), code)
        if newcode != old_code:
            self.while_labels += 1 
        return newcode
    
    
    def restore_loop_placeholders(self, code):
        """
        Replace loop counter value back to the placeholders for future iterations
        """

        code = re.sub(r'loopend(\d+)', r'loopend<LOOP_COUNTER>', code)
        code = re.sub(r'loop(\d+)', r'loop<LOOP_COUNTER>', code)
        return code
        
        
    def p_word_definition(self, p):
        """
        word_definition : ':' USER_DEFINED statements ';'
        """
        
        self.current_word = p[2]
        code = ''.join(p[3])
        args_needed, args_returned = self.count_stack_operations(code)
        self.user_words[p[2]] = (code, args_needed, args_returned)
        p[0] = ""
        
    def count_stack_operations(self, code):
        '''
        Count the number of stack operations needed and returned by a word (used but not necessary)
        '''
        tokens = code.split()
        stack_effect = self.get_stack_args(tokens)
        return stack_effect

    def get_stack_effect(self, token):
        '''
        Returns the number of arguments needed and returned by a token (used but not necessary)
        '''
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
            _, arg_needed, args_returned = self.user_words[token]
            return arg_needed, args_returned
        
        return 0, 0

        
    def get_stack_args(self, token_sequence):
        '''
        Returns the number of arguments needed and returned by a sequence of tokens (used but not necessary)
        '''
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
            code, x, y = self.user_words[p[1]]
            code_looped = self.replace_loop_labels(code, self.while_labels)
                
            code_elsed = self.replace_else_labels(code_looped, self.else_labels)
            
            
            p[0] = code_elsed
            code = self.restore_else_placeholders(code_elsed)
            code = self.restore_loop_placeholders(code)
            self.user_words[p[1]] = (code, x, y)
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
                       | SPACE
                       | num SPACES
        """

        print("p[1]: ", p[1])

        if p[1] == 'cr':
            p[0] = "writeln\n"  
        elif p[1] == 'emit':
            p[0] = "writechr\n"
        elif p[1] == 'space':
            p[0] = 'pushs " "\nwrites\n'
        elif len(p) == 3 and p[2] == 'spaces':
            num_str = p[1]

            num_match = re.match(r'^pushi (\d+)$', num_str)
            times = int(num_match.group(1))
            
            s = ""
            for _ in range(times):
                s += " "
            p[0] = f'pushs "{s}"\nwrites\n'
            
        print("p[0]: ", p[0])
        
        
            
    def p_input_commands(self, p):
        """
        input_command : KEY
                      | S str
                      | CHAR USER_DEFINED
                      | ACCEPT
                      | NUMBER
        """
        if p[1] == 'number':
            p[0] = "atoi\n"
        elif p[1] == 'accept':
            p[0] = "read\n"
            print(p[0])
        elif p[1] == 'char':
            if len(p[2]) > 1:
                print("ERROR: CHAR command only accepts one character")
                sys.exit(1)
            else:
                p[0] = f'pushs "{p[2]}"\nchrcode\n' 
        elif p[1] == 'key':
            p[0] = "read\nchrcode\n"
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
        self.variables_table = VariablesTable()


class VariablesTable:
    """
    Represents a table for FORTH variables to be stored along with his index on the VM heap structure.
    """
    
    
    def __init__(self):
        """
        Initializes an instance of the VariablesTable class.
        """
        self.variables = {}
        self.index_counter = 0

    def add_symbol(self, name):
        """
        Adds a variable to the variables table.

        Parameters:
        - name (str): Name of the variable to be added.
        """
        self.variables[name] = self.index_counter
        self.index_counter += 1

    def get_symbol_index(self, name):
        """
        Retrieves the index of a variable from the symbol table.

        Parameters:
        - name (str): Name of the variable.

        Returns:
        - int or None: Index of the symbol if found, None otherwise.
        """
        return self.variables.get(name, None)
    
    def display(self):
        """
        Displays the symbol table.
        """
        print("Symbol Table:")
        for name, index in self.variables.items():
            print(f"{name}: {index}")
            
            
    def check_variable(self, name):
        """
        Description: Checks if a variable exists in the symbol table.
        
        Parameters:
        - name (str): Name of the variable to check.
            
        Returns: True if the variable exists, `False` otherwise.        
        """
        return name not in self.variables