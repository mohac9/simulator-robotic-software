import parser
import lexer

class ArduinoInterpreter:
    def __init__(self, code):
        self.code = code
        self.variables = {} #Ponerlos en una clase con getter y setter
        self.variables_contents = {} #Ponerlos en una clase con getter y setter
        self.current_line = 0
        self.lines = []
        self.had_runtime_error = False
    
    def visit(self,node): #
        node_type = node['type']
        if node_type == 'Program':
            self.visit_program(node) 
        
    def visit_program(self, node):
        pass

    def visit_assignment(self, node):
        var_name = self.visit_expression(node['left'])
        if var_name.node_type != 'ID': #Cambiar mas tarde
            raise RuntimeError(f"Left side of assignment must be a variable, got {var_name.node_type}.")
        if var_name in self.variables:
            raise RuntimeError(f"Variable '{var_name}' already defined.")
        
        if node['right'].__type__(self.variables) != self.variables[var_name]:
            raise RuntimeError(f"Type mismatch: cannot assign {node['right'].__type__()} to {self.variables[var_name].__type__(self.variables)}.")
        
        contenido = self.visit_expression(node['right'])
        self.variables[var_name] = contenido

    def visit_simple_declaration(self, node):
        var_name = node['name']
        var_type = node['type']
        var_content = node['content']
        
        
        if var_name in self.variables:
            raise RuntimeError(f"Variable '{var_name}' already defined.")
        
        self.variables[var_name] = var_type

        if var_content.__type__(self.variables) != var_type:
            raise RuntimeError(f"Type mismatch: cannot assign {var_content.__type__()} to {var_type}.")
        
        self.variables_contents[var_name] = self.visit_expression(var_content)

        
        




        
        
        

    
 
        

 

       

    