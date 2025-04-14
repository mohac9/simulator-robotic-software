import re
from sly import Parser
from lexer import ArduinoLexer

class ArduinoParser(Parser):
    
    tokens = ArduinoLexer.tokens
        
    #Grammar
    @_('- EOF')
    def start(self, p):
        return ('program', p.program)

    @_('include_directives program_code')
    def program(self, p):
        return ('program', p.include_directives, p.program_code)

    @_('include_directives include')
    def include_directives(self, p):
        return p.include_directives + [p.include]

    @_('include')
    def include_directives(self, p):
        return [p.include]

    @_('INCLUDE STRING_CONST')
    def include(self, p):
        return ('include', p.STRING_CONST)

    @_('INCLUDE "<" ID "." ID ">"')
    def include(self, p):
        return ('include', f'<{p.ID_0}.{p.ID_1}>')

    @_('program_code declaration ";"')
    def program_code(self, p):
        return ('declaration', p.declaration)

    @_('program_code function')
    def program_code(self, p):
        return ('function', p.function)

    @_('program_code define_macro')
    def program_code(self, p):
        return ('define_macro', p.define_macro)

    @_('simple_declaration')
    def declaration(self, p):
        return ('simple_declaration', p.simple_declaration)

    @_('array_declaration')
    def declaration(self, p):
        return ('array_declaration', p.array_declaration)

    @_('qualifier declaration')
    def declaration(self, p):
        return ('qualified_declaration', p.qualifier, p.declaration)

    @_('CONST', 'STATIC')
    def qualifier(self, p):
        return p[0]

    @_('var_type ID "=" expression')
    def simple_declaration(self, p):
        return ('simple_declaration', p.var_type, p.ID, p.expression)

    @_('var_type ID')
    def simple_declaration(self, p):
        return ('simple_declaration', p.var_type, p.ID)

    @_('var_type ID array_index "=" expression')
    def array_declaration(self, p):
        return ('array_declaration', p.var_type, p.ID, p.array_index, p.expression)

    @_('var_type ID array_index "=" array_elements')
    def array_declaration(self, p):
        return ('array_declaration', p.var_type, p.ID, p.array_index, p.array_elements)

    @_('var_type ID array_index')
    def array_declaration(self, p):
        return ('array_declaration', p.var_type, p.ID, p.array_index)

    @_('define_macro')
    def program_code(self, p):
        return ('define_macro', p.define_macro)

    @_('DEFINE ID expression')
    def define_macro(self, p):
        return ('define_macro', p.ID, p.expression)

    @_('DEFINE ID array_elements')
    def define_macro(self, p):
        return ('define_macro', p.ID, p.array_elements)

    @_('"[" "]"')
    def array_index(self, p):
        return ('array_index', [])

    @_('"[" INT_CONST "]"')
    def array_index(self, p):
        return ('array_index', [p.INT_CONST])

    @_('"[" INT_CONST "]" array_index')
    def array_index(self, p):
        return ('array_index', [p.INT_CONST] + p.array_index[1])

    @_('expression')
    def array_elements(self, p):
        return ('array_elements', [p.expression])

    @_('"{" array_elements "}"')
    def array_elements(self, p):
        return ('array_elements', p.array_elements)

    @_('var_type')
    def var_type(self, p):
        return p[0]

    @_('"bool"')
    def var_type(self, p):
        return 'bool'

    @_('"boolean"')
    def var_type(self, p):
        return 'boolean'

    @_('"byte"')
    def var_type(self, p):
        return 'byte'

    @_('"char"')
    def var_type(self, p):
        return 'char'

    @_('"double"')
    def var_type(self, p):
        return 'double'

    @_('"float"')
    def var_type(self, p):
        return 'float'

    @_('"int"')
    def var_type(self, p):
        return 'int'

    @_('"long"')
    def var_type(self, p):
        return 'long'

    @_('"short"')
    def var_type(self, p):
        return 'short'

    @_('"size_t"')
    def var_type(self, p):
        return 'size_t'

    @_('"String"')
    def var_type(self, p):
        return 'String'

    @_('"unsigned int"')
    def var_type(self, p):
        return 'unsigned int'

    @_('"unsigned char"')
    def var_type(self, p):
        return 'unsigned char'

    @_('"unsigned long"')
    def var_type(self, p):
        return 'unsigned long'

    @_('"void"')
    def var_type(self, p):
        return 'void'

    @_('"word"')
    def var_type(self, p):
        return 'word'

    @_('ID')
    def var_type(self, p):
        return p.ID

    # Error handling
    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}, line {p.lineno}")
            self.errok()
        else:
            print("Syntax error at EOF")
    

if __name__ == "__main__":
    lexer = ArduinoLexer()
    parser = ArduinoParser()

    data = '''
    #include <Arduino.h>
    int led = 13;
    void setup() {
        pinMode(led, OUTPUT);
    }
    void loop() {
        digitalWrite(led, HIGH);
        delay(1000);
        digitalWrite(led, LOW);
        delay(1000);
    }
    '''
    tokens = lexer.tokenize(data)
    for i in tokens:
        print(i)
    #result = parser.parse(tokens)
    print(result)