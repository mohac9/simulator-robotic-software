import re
from sly import Parser
from lexer import ArduinoLexer

class ArduinoParser(Parser):
    
    tokens = ArduinoLexer.tokens
    
    precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    )
    
    
    #Grammar rules
    
    #Top level rules
    @_('LBRACE RBRACE')
    def program(self, p):
        return ('program', [])
    
    @_('include_list program_code_list')
    def program(self, p):
        return ('program', p.include_list, p.program_code_list)
    
    @_('')
    def include_list(self, p):
        return []

    @_('include_list include')
    def include_list(self, p):
        return p.include_list + [p.include]
    
    @_('INCLUDE STRING_CONST')
    def include(self, p):
        return ('include', p.STRING_CONST)
    
    @_('')
    def program_code_list(self, p):
        return []
    
    @_('program_code_list program_code')
    def program_code_list(self, p):
        return p.program_code_list + [p.program_code]
    
    @_('declaration SEMICOLON')
    def program_code(self, p):
        return ('declaration', p.declaration)
    
    @_('function')
    def program_code(self, p):
        return ('function_definition', p.function)     
    
    @_('define_macro')
    def program_code(self, p):
        return ('macro_definition', p.define_macro)   
    
    
    #Declaration rules
    @_('simple_declaration')
    def declaration(self, p):
        return ('simple_declaration', p.simple_declaration)
    
    @_('array_declaration')
    def declaration(self, p):
        return ('array_declaration', p.array_declaration)
    
    @_('CONST declaration')
    def declaration(self, p):
        return ('const_declaration', p.declaration)
    
    @_('STATIC declaration')
    def declaration(self, p):
        return ('static_declaration', p.declaration)
    
    @_('var_type ID EQUAL expression ')
    def simple_declaration(self, p):
        return ('simple_declaration', p.var_type, p.ID, p.expression)
    
    @_('var_type ID')
    def simple_declaration(self, p):
        return ('simple_declaration', p.var_type, p.ID, None)
    
    
    @_('var_type ID array_index EQUAL expression')
    def array_declaration(self, p):
        return ('array_declaration_asg_expr', p.var_type, p.ID, p.array_index, p.expression)
       
    @_('var_type ID array_index EQUAL array_elements')
    def array_declaration(self, p):
        return ('array_declaration_asg_elem', p.var_type, p.ID, p.array_index, p.array_elements)           

    @_('var_type ID array_index')
    def array_declaration(self, p):
        return ('array_declare', p.var_type, p.ID, p.array_index, None)
    
    
    #Array rules
    @_('LBRACKET expression RBRACKET')
    def array_index(self, p):
        return ('array_index', p.expression)
    
    @_('LBRACE expression_list RBRACE')
    def array_elements(self, p):
        return ('array_elements', p.expression_list)
    
    #Macro rules
    @_('DEFINE ID EQUAL expression')
    def define_macro(self, p):
        return ('macro_definition', p.ID, p.expression)
    
    @_('DEFINE ID array_elements')
    def define_macro(self, p):
        return ('macro_definition', p.ID, p.array_elements)
    
    #Function rules @dataclasses
    @_('var_type ID LPAREN function_args RPAREN LBRACE sentence_list RBRACE')
    def function(self, p):
        return ('function', p.var_type, p.ID, p.function_args, p.sentence_list)
    
    @_('var_type ID LPAREN RPAREN LBRACE sentence_list RBRACE')
    def function(self, p):  
        return ('function', p.var_type, p.ID, [], p.sentence_list)
    
    @_('function_args COMMA declaration')
    def function_args(self, p):
        return [p.declaration] + p.function_args
    
    @_('declaration')
    def function_args(self, p):
        return [p.declaration]
    
    @_('sentence_list sentence') 
    def sentence_list(self, p):
        return p.sentence_list + [p.sentence]
    
    @_('')
    def sentence_list(self, p):
        return []
    
    #Sentence rules
    @_('declaration SEMICOLON')
    def sentence(self, p):
        return ('dec',p.declaration)
    
    @_('iteration_sentence')
    def sentence(self, p):
        return ('it_sent',p.iteration_sentence)
    
    @_('conditional_sentence')
    def sentence(self, p):
        return ('cond_sent',p.conditional_sentence)
    
    @_('assignment SEMICOLON')
    def sentence(self, p):
        return ('assign',p.assignment)
        
    
    @_('expression SEMICOLON')
    def sentence(self, p):
        return ('expr',p.expression)      
    
    @_('define_macro')
    def sentence(self, p):
        return ('def_macro',p.define_macro)
    
    @_('RETURN expression SEMICOLON')
    def sentence(self, p):
        return ('return', p.expression)
    
    @_('RETURN SEMICOLON')
    def sentence(self, p):
        return ('return', None)
    
    @_('BREAK SEMICOLON')
    def sentence(self, p):
        return ('break', None)
    
    @_('CONTINUE SEMICOLON')
    def sentence(self, p):
        return ('continue', None)
    
    #Assignment rules
    @_('expression EQUAL expression')
    def assignment(self, p):
        return {
            'type': 'assignment',
            'left': p.expression0,
            'right': p.expression1
        }
    
    #Iterative and conditional sentences
    @_('WHILE LPAREN expression RPAREN LBRACE code_block RBRACE')
    def iteration_sentence(self, p):
        return {
            'type': 'while',
            'condition': p.expression,
            'body': p.sentence_list
        }
        
    
    @_('DO code_block WHILE LPAREN expression RPAREN SEMICOLON')
    def iteration_sentence(self, p):
        return {
            'type': 'do_while',
            'condition': p.expression,
            'body': p.sentence_list
        }

    
    @_('FOR LPAREN simple_declaration_optional SEMICOLON expression_optional SEMICOLON expression_optional RPAREN code_block')
    def iteration_sentence(self, p):
        return {
            'type': 'for',
            'initializer': p.simple_declaration_optional,
            'condition': p.expression_optional,
            'increment': p.expression_optional,
            'body': p.code_block
        }
    
    #Auxiliary rules, allows me to ot repeat the for rule several times
    @_('')
    def simple_declaration_optional(self, p):
        return None
    
    @_('simple_declaration')
    def simple_declaration_optional(self, p):
        return p.simple_declaration
    
    @_('')
    def expression_optional(self, p):
        return None
    
    @_('expression')
    def expression_optional(self, p):
        return p.expression
    
    #Conditional sentences
    @_('IF LPAREN expression RPAREN code_block LPAREN ELSE code_block RPAREN')
    def conditional_sentence(self, p):
        return ('if_else', p.expression, p.sentence_list, p.sentence_list1)
    
    @_('IF LPAREN expression RPAREN code_block')
    def conditional_sentence(self, p):
        return ('if', p.expression, p.sentence_list)
    
    #May be necessary to add a if else  
    
    @_('SWITCH LPAREN expression RPAREN LBRACE case_sentence_list RBRACE')
    def conditional_sentence(self, p):
        return ('switch', p.expression, p.case_sentence_list)
    
    
    
    
    #Case sentence
    @_('')
    def case_sentence_list(self, p):
        return []
    
    @_('case_sentence case_sentence_list')
    def case_sentence_list(self, p):
        return [p.case_sentence] + p.case_sentence_list
    
    
    @_('CASE expression COLON sentence_list')
    def case_sentence(self, p):
        return ('case', p.expression, p.sentence_list)
    
    @_('DEFAULT COLON sentence_list')
    def case_sentence(self, p):
        return ('default', p.sentence_list)
    
    
    #Code block
    @_('LBRACE sentence_list RBRACE')
    def code_block(self, p):
        return p.sentence_list
    
    @_('LBRACE RBRACE') #I'm not sure of this one
    def code_block(self, p):
        return []
    
    
    
    
    

        
    #Expression rules
    @_('BOOL_CONST')
    def expression(self, p):
        return ('bool_const', p.BOOL_CONST)
    
    @_('LOW')
    def expression(self, p):
        return ('low', p.LOW)
    
    @_('HIGH')
    def expression(self, p):
        return ('high', p.HIGH)
    
    @_('ANALOG_PIN')
    def expression(self, p):
        return ('analog_pin', p.ANALOG_PIN)
    
    @_('INPUT')
    def expression(self, p):
        return ('input', p.INPUT)
    
    @_('INPUT_PULLUP')
    def expression(self, p):
        return ('input_pullup', p.INPUT_PULLUP)
    
    @_('OUTPUT')
    def expression(self, p):
        return ('output', p.OUTPUT)
    
    @_('HEX_CONST')
    def expression(self, p):
        return ('hex_const', p.HEX_CONST)
    
    @_('OCTAL_CONST')
    def expression(self, p):
        return ('octal_const', p.OCTAL_CONST)
    
    @_('BINARY_CONST')
    def expression(self, p):
        return ('binary_const', p.BINARY_CONST)
    
    @_('INT_CONST')
    def expression(self, p):
        return ('int_const', p.INT_CONST)
    
    @_('FLOAT_CONST')
    def expression(self, p):
        return ('float_const', p.FLOAT_CONST)
    
    @_('CHAR_CONST')
    def expression(self, p):
        return ('char_const', p.CHAR_CONST)
    
    @_('STRING_CONST')
    def expression(self, p):
        return ('string_const', p.STRING_CONST)
    
    @_('ID')
    def expression(self, p):
        return ('id', p.ID)
    
    @_('ID LPAREN expression_list RPAREN')
    def expression(self, p):
        return ('r_expr', p.ID, p.expression_list)
    
    @_('expression "." expression')
    def expression(self, p):
        return ('member_acc', p.expression0, p.expression1)
    
    @_('ID LBRACKET expression_list RBRACKET')
    def expression(self, p):
        return ('array_name', p.ID, p.expression_list)
    
    # Auxiliary expression_list rule
    @_('expression_list COMMA expression')
    def expression_list(self, p):
        return p.expression_list + [p.expression]

    
    @_('expression')
    def expression_list(self, p):
        return [p.expression]
    

    @_('expression LPAREN parameter RPAREN')
    def expression(self, p):
        return ('function_call', p.expression, p.parameter)

    @_('expression LPAREN RPAREN')
    def expression(self, p):
        return ('function_call', p.expression, None)

    @_('conversion')
    def expression(self, p):
        return ('conversion', p.conversion)

    @_('PLUS PLUS expression')
    def expression(self, p):
        return ('increment', p.expression)

    @_('MINUS MINUS expression')
    def expression(self, p):
        return ('decrement', p.expression)

    @_('NOT expression')
    def expression(self, p):
        return ('not', p.expression)

    @_('BITWISE_NOT expression')
    def expression(self, p):
        return ('bitwise_not', p.expression)

    @_('expression MULTIPLY expression')
    def expression(self, p):
        return ('mul', p.expression0, p.expression1)

    @_('expression DIVIDE expression')
    def expression(self, p):
        return ('div', p.expression0, p.expression1)

    @_('expression MODULUS expression')
    def expression(self, p):
        return ('mod', p.expression0, p.expression1)

    @_('expression PLUS expression')
    def expression(self, p):
        return ('sum', p.expression0, p.expression1)

    @_('expression MINUS expression')
    def expression(self, p):
        return ('sub', p.expression0, p.expression1)

    @_('expression BITWISE_RIGHT_SHIFT expression')
    def expression(self, p):
        return ('bit_shift_r', p.expression0, p.expression1)

    @_('expression BITWISE_LEFT_SHIFT expression')
    def expression(self, p):
        return ('bit_shift_l', p.expression0, p.expression1)

    @_('expression LT expression')
    def expression(self, p):
        return ('less_than', p.expression0, p.expression1)

    @_('expression LE expression')
    def expression(self, p):
        return ('less_than_eq', p.expression0, p.expression1)

    @_('expression GT expression')
    def expression(self, p):
        return ('greater_than', p.expression0, p.expression1)

    @_('expression GE expression')
    def expression(self, p):
        return ('greater_than_eq', p.expression0, p.expression1)

    @_('expression EQ expression')
    def expression(self, p):
        return ('equal', p.expression0, p.expression1)

    @_('expression NE expression')
    def expression(self, p):
        return ('ne', p.expression0, p.expression1)

    @_('expression BITWISE_AND expression')
    def expression(self, p):
        return ('bitwise_and', p.expression0, p.expression1)

    @_('expression BITWISE_XOR expression')
    def expression(self, p):
        return ('bitwise_xor', p.expression0, p.expression1)

    @_('expression BITWISE_OR expression')
    def expression(self, p):
        return ('bitwise_or', p.expression0, p.expression1)

    @_('expression AND expression')
    def expression(self, p):
        return ('logical_and', p.expression0, p.expression1)

    @_('expression OR expression')
    def expression(self, p):
        return ('logical_or', p.expression0, p.expression1)

    @_('expression compound_operator expression')
    def expression(self, p):
        return ('compound_assignment', p.expression0, p.compound_operator, p.expression1)

    @_('MODULUS EQ')
    @_('BITWISE_AND EQ')
    @_('MULTIPLY EQ')
    @_('PLUS EQ')
    @_('MINUS EQ')
    @_('DIVIDE EQ')
    @_('BITWISE_XOR EQ')
    @_('BITWISE_OR EQ')
    def compound_operator(self, p):
        return p[0]

    # Conversion rules
    @_('LPAREN UNSIGNED_INT RPAREN expression')
    def conversion(self, p):
        return ('conversion', 'unsigned int', p.expression)

    @_('LPAREN UNSIGNED_LONG RPAREN expression')
    def conversion(self, p):
        return ('conversion', 'unsigned long', p.expression)

    @_('LPAREN type_convert RPAREN expression')
    def conversion(self, p):
        return ('conversion', p.type_convert, p.expression)

    @_('STRING LPAREN expression RPAREN')
    def conversion(self, p):
        return ('conversion', 'String', p.expression)

    @_('type_convert LPAREN expression RPAREN')
    def conversion(self, p):
        return ('conversion', p.type_convert, p.expression)

    # Type conversion rules
    @_('BYTE')
    @_('CHAR')
    @_('FLOAT')
    @_('INT')
    @_('LONG')
    @_('WORD')
    def type_convert(self, p):
        return p[0]

    # Parameter rules
    @_('expression_list')
    def parameter(self, p):
        return p.expression_list

   
    
    #Variable type rules
    @_('BOOL', 'BOOLEAN', 'BYTE', 'CHAR', 'DOUBLE', 'FLOAT', 'INT', 'LONG', 'SHORT', 'SIZE_T', 'STRING', 
        'UNSIGNED_INT', 'UNSIGNED_CHAR', 'UNSIGNED_LONG', 'VOID', 'WORD', 'ID')
    def var_type(self, p):
         return p[0]

   #Parenthesis rules
    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return p.expression
    
    
    #Symbols
    @_('EQUAL')
    def symbol(self, p):
        return p.EQUAL
    
    @_('NOT_EQUAL')
    def symbol(self, p):
        return p.NOT_EQUAL
    
    @_('SEMICOLON')
    def symbol(self, p):
        return p.SEMICOLON    
    
    @_('NUMBER')
    def expression(self, p):
        return ('int_const', p.NUMBER)

def print_tree(node, indent=0):
    if isinstance(node, tuple):
        print('  ' * indent + str(node[0]) + '{')
        for child in node[1:]:
            print_tree(child, indent + 1)
        print('  ' * indent + '}')
    elif isinstance(node, list):
        for item in node:
            print_tree(item, indent)
    else:
        print('  ' * indent + str(node)) 
    

        
# Convertir el string en un arbol de sintaxis

if __name__ == '__main__':
    data = ''' 
    #include "Arduino.h"
    int a = 0;
    '''
    lexer = ArduinoLexer()
    print("----------------------------------")
    for i in lexer.tokenize(data):
        print(f'#{i.lineno} {i.type} {i.value}')
    print("----------------------------------")
    parser = ArduinoParser()
    result = parser.parse(lexer.tokenize(data))
    print_tree(result)
    
    