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
        if isinstance(node, ta.program):
            self.visit_program(node)
        
        
    def visit_program(self, node):
        pass

    def visit_assignment(self, node):
        
        if node.__class__() == ta.assignment:
            node.execute(self.variables)
        else:
            raise RuntimeError(f"Unknown assignment type: {node.__class__()}.")

    def visit_simple_declaration(self, node):
        if node.__class__() == ta.simple_declaration:
            node.execute(self.variables)
        else:
            raise RuntimeError(f"Unknown simple declaration type: {node.__class__()}.")
        
    def visit_expression(self, node):
        if node.__class__() == ta.binary_operation:
            return node.execute()
        else:
            raise RuntimeError(f"Unknown expression type: {node.__class__()}.")

    
 
        

 

       

    