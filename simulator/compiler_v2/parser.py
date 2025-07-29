import re
from sly import Parser
from lexer import ArduinoLexer
import typesArduino as ta



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
        return ta.program([], [])
    
    @_('include_list program_code_list')
    def program(self, p):
        return ta.program(p.include_list, p.program_code_list)
        
    @_('')
    def include_list(self, p):
        return ta.include_list([])

    @_('include_list include')
    def include_list(self, p):
        p.include_list.append(p.include)
        return p.include_list

    @_('INCLUDE STRING_CONST')
    def include(self, p):
        return ta.include(p.STRING_CONST)
    
    @_('')
    def program_code_list(self, p):
        return ta.program_code_list([])
    
    @_('program_code_list program_code')
    def program_code_list(self, p):
        p.program_code_list.append(p.program_code)
        return p.program_code_list
    
    @_('declaration SEMICOLON')
    def program_code(self, p):
        return ta.program_code(p.declaration)
    
    @_('assignment SEMICOLON')
    def program_code(self, p):  #May contradict the grammar
        return ta.program_code(p.assignment)
    
    @_('function')
    def program_code(self, p):
        return ta.program_code(p.function)    
    
    @_('define_macro')
    def program_code(self, p):
        return ta.program_code(p.define_macro)
    
    @_('sentence_list')
    def program_code(self, p):
        return ta.program_code(p.sentence_list)
    
    #Declaration rules
    @_('simple_declaration')
    def declaration(self, p):
        return ta.declaration(p.simple_declaration)
    
    #TODO: Change this to a ta.* return
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
        return ta.simple_declaration(p.ID, p.var_type, p.expression)

    @_('var_type ID')
    def simple_declaration(self, p):
        return ta.simple_declaration(p.ID, p.var_type, None)


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
        return ta.function(p.var_type, p.ID, p.function_args, p.sentence_list)
    
    @_('var_type ID LPAREN RPAREN LBRACE sentence_list RBRACE')
    def function(self, p):  
        return ta.function(p.var_type, p.ID, None, p.sentence_list)
    
    @_('function_args COMMA declaration')
    def function_args(self, p):
        return p.function_args.append(p.declaration)
    
    
    @_('declaration')
    def function_args(self, p):
        return ta.function_args([p.declaration])
    
    @_('sentence_list sentence') 
    def sentence_list(self, p):
        new_sentences = p.sentence_list.sentences.copy()
        new_sentences.append(p.sentence)
        return ta.sentence_list(new_sentences)
        
    
    @_('')
    def sentence_list(self, p):
        return ta.sentence_list([])
    
    #Sentence rules
    @_('declaration SEMICOLON')
    def sentence(self, p):
        return ta.sentence(p.declaration)
        
    
    @_('iteration_sentence')
    def sentence(self, p):
        return ta.sentence(p.iteration_sentence)
        
    
    @_('conditional_sentence')
    def sentence(self, p):
        return ta.sentence(p.conditional_sentence)
    
    @_('assignment SEMICOLON')
    def sentence(self, p):
        return ta.sentence(p.assignment)
        
    
    @_('expression SEMICOLON')
    def sentence(self, p):
        return ta.sentence(p.expression)     
    
    @_('define_macro')
    def sentence(self, p):
        return ta.sentence(p.define_macro)
    
    @_('RETURN expression SEMICOLON')
    def sentence(self, p):
        pass
        
    
    @_('RETURN SEMICOLON')
    def sentence(self, p):
        return ('return', None)
    
    @_('BREAK SEMICOLON')
    def sentence(self, p):
        return ta.break_statement()
    
    @_('CONTINUE SEMICOLON')
    def sentence(self, p):
        return ('continue', None)
    
    #Assignment rules
    @_('ID EQUAL expression')
    def assignment(self, p):
        return ta.assignment(p.ID, p.expression)
        
    
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
        return ta.if_statement(p.expression, p.code_block0, p.code_block1)
    
    @_('IF LPAREN expression RPAREN code_block')
    def conditional_sentence(self, p):
        return ta.if_statement(p.expression, p.code_block)

    #May be necessary to add a if else

    @_('SWITCH LPAREN expression RPAREN LBRACE case_sentence_list RBRACE')
    def conditional_sentence(self, p):
        return ta.switch_statement(p.expression, p.case_sentence_list)
    
    
    
    
    #Case sentence
    @_('')
    def case_sentence_list(self, p):
        return ta.case_sentence_list([])
    
    @_('case_sentence_list case_sentence')
    def case_sentence_list(self, p):
        return p.case_sentence_list.append(p.case_sentence)
        
        
    
    
    @_('CASE expression COLON sentence_list')
    def case_sentence(self, p):
        return ta.case_sentence(p.expression, p.sentence_list)
    
    @_('DEFAULT COLON sentence_list') # Ask how to implement this
    def case_sentence(self, p):
        return ta.case_sentence(None, p.sentence_list)  # Default case, no expression, just the body


    #Code block
    @_('LBRACE sentence_list RBRACE')
    def code_block(self, p):
        return p.sentence_list
       
    @_('LBRACE RBRACE') #I'm not sure of this one
    def code_block(self, p):
        return ta.sentence_list([])
    
    
    
    
    

        
    #Expression rules
    @_('BOOL_CONST')
    def expression(self, p):
        return ta.Bool(p.BOOL_CONST)
    
    @_('TRUE')
    def expression(self, p):
        return ta.Bool(True)
    @_('FALSE')
    def expression(self, p):
        return ta.Bool(False)
    
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
        return ta.Int(p.INT_CONST)
    
    @_('FLOAT_CONST')
    def expression(self, p):
        return ta.Float(p.FLOAT_CONST)
    
    @_('CHAR_CONST')
    def expression(self, p):
        return ('char_const', p.CHAR_CONST)
    
    @_('STRING_CONST')
    def expression(self, p):
        return ('string_const', p.STRING_CONST)
    
    @_('ID')
    def expression(self, p):
        return ta.Object(p.ID)
    
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
        return ta.unary_operation(p.expression, ta.Number.__next__)

    @_('MINUS MINUS expression')
    def expression(self, p):
        return ta.unary_operation(p.expression, ta.Number.__prev__)
        

    @_('NOT expression')
    def expression(self, p):
        return ta.unary_operation(p.expression, ta.Bool.__not__)

    @_('BITWISE_NOT expression')
    def expression(self, p):
        return ta.unary_operation(p.expression, ta.Number.__bitwise_not__)

    @_('expression MULTIPLY expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, lambda a, b: a.__mul__(b))

    @_('expression DIVIDE expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, lambda a, b: a.__truediv__(b))

    @_('expression MODULUS expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, lambda a, b: a.__mod__(b))

    @_('expression PLUS expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, lambda a, b: a.__add__(b)) #Usar objetos de TypesArduino

    @_('expression MINUS expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0,p.expression1, lambda a, b: a.__sub__(b)) #Usar objetos de TypesArduino

    @_('expression BITWISE_RIGHT_SHIFT expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__bit_shift_r__)

    @_('expression BITWISE_LEFT_SHIFT expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__bit_shift_l__)

    @_('expression LT expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__lt__)

    @_('expression LE expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__le__)

    @_('expression GT expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__gt__)

    @_('expression GE expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__ge__)

    @_('expression EQ expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__eq__)

    @_('expression NE expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__ne__)

    @_('expression BITWISE_AND expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__bitwise_and__)

    @_('expression BITWISE_XOR expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__bitwise_xor__)

    @_('expression BITWISE_OR expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__bitwise_or__)

    @_('expression AND expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__and__)

    @_('expression OR expression')
    def expression(self, p):
        return ta.binary_operation(p.expression0, p.expression1, ta.Number.__or__)

    #TODO: Change later to use objects from typesArduino
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
        return ta.parenthesis(p.expression)
    
    
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
    
    
def print_tree_v2(node, indent=0):
    print(' ' * indent, node)
    try:
        children_list = node.children()
    except AttributeError:
        return
    if children_list:
        for child in children_list:
            print_tree_v2(child, indent + 2)
    else:
        print(' ' * (indent + 2), 'No children')
    
    

        
# Convertir el string en un arbol de sintaxis

if __name__ == '__main__':
    data = code = """
    int a;
    int foo(int x, char y){
        z = x;
    }
    
    """
    lexer = ArduinoLexer()
    print("----------------------------------")
    for i in lexer.tokenize(data):
        print(f'#{i.lineno} {i.type} {i.value}')
    print("----------------------------------")
    parser = ArduinoParser()
    result = parser.parse(lexer.tokenize(data))
    #print_tree(result)
    print("----------------------------------")
    print_tree_v2(result)
    
   