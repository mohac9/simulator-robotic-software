import parser
from lexer import ArduinoLexer
import typesArduino as ta
import environment

        


class ArduinoInterpreter:
    def __init__(self, code):
        self.code = code
        self.current_line = 0
        self.env = None
        self.lines = []
        self.had_runtime_error = False
        
        print(code)
        lexer = ArduinoLexer()
        self.tokens = lexer.tokenize(code)
        self.parser = parser.ArduinoParser()
        self.parser_object = self.parser.parse(self.tokens)
        
        
    
    def visit(self,node,env): #
        node.execute(env)
        
    def get_variables(self):
        self.env.get_all_variables()
        print("Variables in the environment:")
        for var in self.env.get_all_variables():
            print(f"Name: {var['name']}, Type: {var['type']}, Content: {var['content']}")
       
    
    
    
    def show_tree(self):
        parser.print_tree_v2(self.parser_object)
        parser.print_tree(self.parser_object)
        print(self.parser_object)
    
    
    
    def run(self,node):
        self.env = environment.Environment()
        node.execute(self.env)
        
        pass
    

if __name__ == '__main__':
    # Binary operations are correctly handled
    # Variables are correctly defined and assigned
    # Type conversion is correctly handled(Internally)
    code = """
    int a = 5;
    int b = 10;
    a = a + 2;
    if( a < b ) {
        b = b  + 1;
    }
    
    """
    interpreter = ArduinoInterpreter(code)
    #interpreter.show_tree()
    interpreter.run(interpreter.parser_object)
    interpreter.get_variables()

        
        
        
    