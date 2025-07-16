class Environment:
    def __init__(self,parent_env=None):
        self.variables = {} #Key: variable name, Value: variable type
        self.variables_contents = {} #Key: variable name, Value: variable content
        self.parent_env = parent_env
        
    def set_variable(self, name, var_type, content=None):
        if name in self.variables:
            raise RuntimeError(f"Variable '{name}' already defined.")
        self.variables[name] = var_type
        self.variables_contents[name] = content
        
        
    def get_variable_type(self,name):
        return  self.variables[name]
    
    def get_variable_contents(self,name):
        return self.variables_contents[name]
    
    def modify_variable(self,name,content):
        self.variables_contents[name] = content
        
    def cast_type(self,name,new_type):
        self.variables[name] = name
        
    def get_all_variables(self):
        return [
            {"name": name, "type": self.variables[name], "content": self.variables_contents[name]}
            for name in self.variables
        ]
    #TODO: Search parents variables for env inside functions
    def search_parents(self,name):
        pass
        