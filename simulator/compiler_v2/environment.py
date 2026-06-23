import inspect

try:
    import libraries.standard as std
    import libraries.keyboard as keyboard
    import libraries.libs as libs
    import libraries.string as string
    import libraries.servo as servo
    import libraries.serial as serial
except ImportError:
    import sys
    from pathlib import Path


    simulator_dir = Path(__file__).resolve().parent.parent

    if str(simulator_dir) not in sys.path:
        sys.path.insert(0, str(simulator_dir))

    import libraries.standard as std
    import libraries.keyboard as keyboard
    import libraries.libs as libs
    import libraries.string as string
    import libraries.servo as servo
    import libraries.serial as serial

class Environment:
    def __init__(self,parent_env=None, board=None):
        self.board = board if board is not None else (parent_env.board if parent_env else None)
        self.variables = {} #Key: variable name, Value: variable type
        self.variables_contents = {} #Key: variable name, Value: variable content
        self.parent_env = parent_env #May be eliminated in the future, not used yet
        self.functions = {} # key: Signature(name + args) , value: function object
        self.libraries = {} # key: library name, value: library module   
        self.built_in_functions = {} # key: function name, value: function object
        self.lib_functions = {} #key: lib.function_name, value: function object

        self.types ={}  #key: type name, value: get_methods()
        self.registered_classes = {} #key: type class, value:class

        #Hacer registro de funciones built in
        self.register_built_in()

        #Dict with the hardware components
        self.hardware_elements = {} #key: hw_name, value:object

        

        #Debugger related attributes
        self.debugger = None
        if parent_env is not None:
            self.call_stack = self.parent_env.call_stack
            self.debugger = getattr(self.parent_env, 'debugger', None)
        else:
            self.call_stack = []
            #self.debugger = None

    def add_board(self,board):
        print("-"*20)
        print(self.board,board)
        self.board = board

    #Auxilliary functions
    def get_name_from_signature(self,signature):
        return signature.split('#')[0]
        
        
    #TODO: Check collisions with function names, done   
    def set_variable(self, name, var_type, content=None):
        if name in self.variables:
            raise RuntimeError(f"Variable '{name}' already defined.")
        
        self.variables[name] = var_type
        self.variables_contents[name] = content
        

    def is_class(self, var_type):
        print("*"*10)
        print(self.registered_classes)
        return var_type in self.registered_classes

    #Changed to modify the hd of the arduino robot
    def set_instance(self,name,var_type):
        
        if name in self.variables:
            raise RuntimeError(f"Variable '{name}' already defined.")
        
        class_object = self.registered_classes[var_type]
        
        
        instance = class_object(self.board)
        print(f"Se ha declarado la instancia:{instance} de tipo:{type(instance)}")

        #instance = self.hardware_elements[name]

        self.variables[name] = var_type
        self.variables_contents[name] = instance
        
        


        
    
    def get_variable_type(self,name):
        if name in self.variables:
            return  self.variables[name]
        
        if self.parent_env is not None:
            return self.parent_env.get_variable_type(name)
        raise RuntimeError(f"Variable '{name}' not defined.")


    
    def get_variable_contents(self,name):
        if name in self.variables_contents:
            return self.variables_contents[name]
        if self.parent_env is not None:
            return self.parent_env.get_variable_contents(name)
        raise RuntimeError(f"Variable '{name}' not defined.")

    def modify_variable(self,name,content):
        if name in self.variables_contents:
            self.variables_contents[name] = content
            return
        if self.parent_env is not None:
            self.parent_env.modify_variable(name,content)
            return
        raise RuntimeError(f"Variable '{name}' not defined before the assignment.")
        
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

        
    #TODO: Eliminar, si despues de la comprobación se comprueba que no se usa en ningun lado, eliminar
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
        f"El lib es {lib}"
        if lib == "Servo":       
            prefijo = "servo"

            self.registered_classes["Servo"] = servo.Servo
            self.lib_functions.update({
                
                

                f"{lib}.{name}": getattr(servo.Servo, name)
                for name in dir(servo.Servo)
                if not name.startswith('__') and callable(getattr(servo.Servo, name))

                
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
        
        if lib == "Serial":
            self.lib_functions.update({
                f"serial.{name}": func for name, func in inspect.getmembers(serial, inspect.isfunction)
            })

        #self.lib_functions = {str (k).lower():self.lib_functions[k] for k in self.lib_functions}
        print(f"Registered library '{lib}' with functions: {', '.join(name for name in self.lib_functions if name.startswith(lib + '.'))}")
        
        
        
    def define_function(self, name, func):
        self.built_in_functions[name] = func

    def add_hw_element(self,key,object):
        self.hardware_elements[key] = object

    #Debugger setter
    def activate_debug_mode(self,debugger):
        self.debugger = debugger
    
        



    

