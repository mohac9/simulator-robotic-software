import re
from sly import Parser
from lexer import ArduinoLexer

class ArduinoParser(Parser):
    
    tokens = ArduinoLexer.tokens
    
    precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    )
    
    
    #Grammar rules
    
    #Top level rules
    
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
    
    @_('')
    
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
    
    #Function rules
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
        return p.declaration
    #TODO
    
    
    
    
    #Expression rules
    @_('expression')
    def statement(self, p):
        return p.expression
    
    
    @_('expression "+" expression')
    @_('expression "-" expression')
    @_('expression "*" expression')
    @_('expression "/" expression')
    def expression(self, p):
        return p.expression0, p[1], p.expression1
    
    @_('NUMBER')
    def expression(self, p):
        return int(p.NUMBER)

    @_('var_type ID EQUAL expression SEMICOLON')
    def statement(self, p):
        return ('declare_assign', p.var_type, p.ID, p.expression)
    
    
    @_('expression')
    def expression_list(self, p):
        return [p.expression]
    
    @_('expression_list COMMA expression')
    def expression_list(self, p):
        return p.expression_list + [p.expression]
    

    
    
    
    #Data types
    @_('INT')
    def var_type(self, p):
        return p.INT
    
    @_('FLOAT')
    def var_type(self, p):
        return p.FLOAT
    
    @_('CHAR')
    def var_type(self, p):
        return p.CHAR
    
    @_('STRING')
    def var_type(self, p):
        return p.STRING
    
    @_('BOOL')
    def var_type(self, p):
        return p.BOOL
    
    @_('VOID')
    def var_type(self, p):
        return p.VOID
    
    @_('ID')
    def var_type(self, p):
        return p.ID
    
    

    #Conversion functions
    
    
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
    
    
        
    #Variable declaration

if __name__ == '__main__':
    data = ''' 
    #include "Arduino.h"
    int i = 0; '''
    lexer = ArduinoLexer()
    print("----------------------------------")
    for i in lexer.tokenize(data):
        print(f'#{i.lineno} {i.type} {i.value}')
    print("----------------------------------")
    parser = ArduinoParser()
    result = parser.parse(lexer.tokenize(data))
    print(result)