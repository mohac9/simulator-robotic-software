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
    
    @_('include_list program_code')
    def program(self, p):
        return ('program', p.include_list, p.program_code)
    
    @_('')
    def include_list(self, p):
        return []

    @_('include_list include')
    def include_list(self, p):
        return p.include_list + [p.include]
    
    @_('#INCLUDE STRING_CONST')
    def include(self, p):
        return ('include', p.STRING_CONST)
    
    @_('')
    def program_code(self, p):
        return []
    
    @_('program_code statement')
    def program_code(self, p):
        return p.program_code + [p.statement]
    
    
        
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