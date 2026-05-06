import inspect
import libraries.standard as std
import libraries.keyboard as keyboard
import libraries.libs as libs
import libraries.string as string
import libraries.servo as servo



class Environment:
    def __init__(self,parent_env=None):
        self.variables = {} #Key: variable name, Value: variable type
        self.variables_contents = {} #Key: variable name, Value: variable content
        self.parent_env = parent_env #May be eliminated in the future, not used yet
        self.functions = {} # key: Signature(name + args) , value: function object
        self.libraries = {} # key: library name, value: library module   
        self.built_in_functions = {} # key: function name, value: function object
        self.built_in_functions = {}
        self.lib_functions = {} #key: lib.function_name, value: function object
        

        #Hacer registro de funciones built in
        self.register_built_in()

        #Debugger related attributes
        if parent_env is not None:
            self.call_stack = self.parent_env.call_stack
            self.debugger = getattr(self.parent_env, 'debugger', None)
        else:
            self.call_stack = []
            self.debugger = None

    #Auxilliary functions
    def get_name_from_signature(self,signature):
        return signature.split('#')[0]
        
        
    #TODO: Check collisions with function names, done   
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
            
    
    def set_function(self,signature, function_object):
        #TODO: Permitir que se ejecuten despues comparando tanto llave y contenido si son iguales no hay error en runtime
        if signature in self.functions or self.get_name_from_signature(signature) in self.variables:
            raise RuntimeError(f"Function '{signature}' already defined.")
        self.functions[signature] = function_object
        
    def get_function(self,signature):
        if signature in self.functions:
            return self.functions[signature]
        if self.parent_env is not None:
            return self.parent_env.get_function(signature)
        raise KeyError(f"Function '{signature}' not found.")
    
    def get_all_functions(self):
        return [
            {"signature": signature, "function_object": self.functions[signature]}
            for signature in self.functions
        ]
    
    def register_library(self, name, library_module):
        self.libraries[name] = library_module

        
    def call_library_function(self, library_name, function_name, args):
        """Call a function from a registered library"""
        if library_name in self.libraries:
            lib = self.libraries[library_name]
            if hasattr(lib, function_name):
                func = getattr(lib, function_name)
                return func(*args)
            else:
                # Try class-based library
                if hasattr(lib, library_name):
                    lib_class = getattr(lib, library_name)
                    lib_instance = lib_class()
                    if hasattr(lib_instance, function_name):
                        func = getattr(lib_instance, function_name)
                        return func(*args)
        
        raise Exception(f"Library function {library_name}.{function_name} not found")
    
    
    #TODO: Añadir todas las funciones built in
    def register_built_in(self):
        self.built_in_functions = {
            name: func for name, func in inspect.getmembers(std, inspect.isfunction)
            }
        
    def register_lib(self, lib):
        if lib == "Servo":
            self.lib_functions.update({
                f"servo.{name}": func for name, func in inspect.getmembers(servo, inspect.isfunction)
            })
        if lib == "Keyboard":
            self.lib_functions.update({
                f"keyboard.{name}": func for name, func in inspect.getmembers(keyboard, inspect.isfunction)
            })
        if lib == "String":
            self.lib_functions.update({
                f"string.{name}": func for name, func in inspect.getmembers(string, inspect.isfunction)
            })
        if lib == "Libs":
            self.lib_functions.update({
                f"libs.{name}": func for name, func in inspect.getmembers(libs, inspect.isfunction)
            })
        

        
        
        
    def define_function(self, name, func):
        self.built_in_functions[name] = func


    


