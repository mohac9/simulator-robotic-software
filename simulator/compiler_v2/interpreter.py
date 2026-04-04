import sys
import os

try:
    from . import parser
    from .lexer import ArduinoLexer
    from . import typesArduino as ta
    from . import environment
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import parser
    from lexer import ArduinoLexer
    import typesArduino as ta
    import environment


import libraries.standard as standard
import libraries.serial as serial
import libraries.string as string_lib
import libraries.servo as servo
        


class ArduinoInterpreter:
    def __init__(self, code):
        self.code = code
        self.current_line = 0
        self.env = None
        self.lines = []
        self.had_runtime_error = False
        
        # This part is responsible for tokenizing the code and parsing it into an AST
        lexer = ArduinoLexer()
        self.tokens = lexer.tokenize(code)
        self.parser = parser.ArduinoParser()
        self.parser_object = self.parser.parse(self.tokens)

        # This part is responsible with the communication with the debugger
        self.line = 0
        
        
        
    #Todo: Delete visit if not used in any part
    def visit(self,node,env): 
        node.execute(env)
        
    
    
    
    
    def run(self,node):
        self.env = environment.Environment()
        
        node.execute(self.env)
        
        pass

    def register_libraries(self, board=None, console=None):
        import libraries.standard as standard
        import libraries.serial as serial
        import libraries.string as string_lib
        import libraries.servo as servo
        
        if board:
            standard.board = board
        if console:
            serial.cons = console
            
        self.env.register_library('Serial', serial)
        self.env.register_library('String', string_lib)
        self.env.register_library('Servo', servo)
        self.env.register_library('Standard', standard)
        
        for func_name in dir(standard):
            if not func_name.startswith('_'):
                func = getattr(standard, func_name)
                if callable(func):
                    self.env.define_function(func_name, func)


    #METHODS FOR DEBUGGING PURPOSES, later will be adapted to the debugger interface 

    def get_variables(self):
        self.env.get_all_variables()
        print("Variables in the environment:")
        for var in self.env.get_all_variables():
            print(f"Name: {var['name']}, Type: {var['type']}, Content: {var['content']}")
       
    def get_functions(self):
        print("Funtions in the environment:")
        for func in self.env.get_all_functions():
            print(f"Signature:{func['signature']}")
    
    def show_tree(self):
        parser.print_tree_v2(self.parser_object)
        parser.print_tree(self.parser_object)
        print(self.parser_object)


if __name__ == '__main__':
    import parser
    from lexer import ArduinoLexer
    import typesArduino as ta
    import environment
    # Binary operations are correctly handled
    # Variables are correctly defined and assigned
    # Type conversion is correctly handled(Internally)
    # Break are correctly implemented
    
    code = """
        int res;
        res = map(25, 0, 100, 0, 1000);

        
    
    """
    interpreter = ArduinoInterpreter(code)
    interpreter.register_libraries()
    interpreter.run(interpreter.parser_object)
    interpreter.get_variables()
    interpreter.get_functions()

        
        
        
    