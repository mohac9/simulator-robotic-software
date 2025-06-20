import parser
import lexer
import typesArduino as ta
import environment

        


class ArduinoInterpreter:
    def __init__(self, code):
        self.code = code
        env = environment.Environment()
        self.current_line = 0
        self.lines = []
        self.had_runtime_error = False
    
    def visit(self,node): #
        node.execute(self.env)
        
    def get_variables(self):
        return self.env.variables
    
    def run():
        pass
        
        
        
        
    