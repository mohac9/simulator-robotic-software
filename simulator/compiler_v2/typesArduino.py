try:
    # When imported as part of a package
    from . import environment
except ImportError:
    # When run directly as a script
    import environment

class Metatype(type):
    _types = {}
    def __new__(cls, name, bases, attrs):
        cls = super().__new__(cls, name, bases, attrs)
        if name  != 'BaseType':
            Metatype._types[name] = cls
        return cls
    @classmethod
    def get_type(cls, name):
        return cls._types.get[name]
    
    def execute(self, env):
        return self
    
    
    


class BaseType(metaclass=Metatype):
    
    
    def __add__(self, other):
        return NotImplemented
    
    def __str__(self):
        return self.__class__.__name__ # for debugging purposes
    
    def children(self):
        return None
    
    def execute(self, env): #For easier implementation of the interpreter
        return self
    

class parserTypes:
    def __init__(self):
        self.children_list = []
        
    def children(self):
        return self.children_list
    
    
type_priority = { 
    'bool': 0, 
    'Int': 1,
    'Float': 2,
    'Double': 3
}
        
def promote(a,b):
    ta = a.__class__.__name__
    tb = b.__class__.__name__

    if ta == tb:
        return a, b
    if type_priority[ta] > type_priority[tb]:
        return a, b.cast_to(ta)
    elif type_priority[ta] < type_priority[tb]:
        return a.cast_to(tb), b
    

class Number(BaseType): #I'm not sure if this is needed
    def __init__(self, value):
        self.value = value
    
    def binary_operation(self, other, operation):
        a, b = promote(self,other)
        return operation(a,b)
    
    def __value__(self):
        return self.value
    
    # Arithmetic operators
    def __add__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value + b.value))
        return self.__class__(value)
    def __sub__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value - b.value))
        return self.__class__(value)
    def __mul__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value * b.value))
        return self.__class__(value)
    def __truediv__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value / b.value))
        return self.__class__(value)
    def __floordiv__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value // b.value))
        return self.__class__(value)
    def __mod__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value % b.value))
        return self.__class__(value)
    def __pow__(self, other):
        value = self.binary_operation(other, lambda a, b: (a.value ** b.value))
        return self.__class__(value)
    def __neg__(self):
        value = self.binary_operation(self, lambda a, b: (-a.value))
        return self.__class__(value)
    
    # Arithmetic unary operators

    def __abs__(self):
        value = abs(self.value)
        return self.__class__(value)
    
    def __prev__(self):
        value = self.value - 1
        return self.__class__(value)
    
    def __next__(self):
        value = self.value + 1
        return self.__class__(value)
    

    # Bitwise operators
    def __bit_shift_r__(self, other):
        result = self.binary_operation(other, lambda a, b: (a.value >> b.value))
        return self.__class__(result)

    def __bit_shift_l__(self, other):
        result = self.binary_operation(other, lambda a, b: (a.value << b.value))
        return self.__class__(result)
    
    def __bitwise_and__(self, other):
        result = self.binary_operation(other, lambda a, b: (a.value & b.value))
        return self.__class__(result)

    def __bitwise_or__(self, other):
        result = self.binary_operation(other, lambda a, b: (a.value | b.value))
        return self.__class__(result)

    def __bitwise_xor__(self, other):
        result = self.binary_operation(other, lambda a, b: (a.value ^ b.value))
        return self.__class__(result)
    
    def __bitwise__not__(self):
        result = ~self.value
        return self.__class__(result)
    
    # Comparison operators
    def __eq__(self, other):
        a, b = promote(self, other)
        return Bool(a.value == b.value)
    def __ne__(self, other):
        a, b = promote(self, other)
        return Bool(a.value != b.value)
    def __lt__(self, other):
        a, b = promote(self, other)
        return Bool(a.value < b.value)
    def __le__(self, other):
        a, b = promote(self, other)
        return Bool(a.value <= b.value)
    def __gt__(self, other):
        a, b = promote(self, other)
        return Bool(a.value > b.value)
    def __ge__(self, other):
        a, b = promote(self, other)
        return Bool(a.value >= b.value)
    

    def __str__(self):
        return f"Number({self.value})"
    
class Byte(Number):
    def __init__(self, value):
        if 0 <= value <= 255:
            self.value = value
        else:
            raise ValueError("Byte value must be between 0 and 255")
        
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(int(self.value))
        elif target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Byte'
    
    def __str__(self):
        return f"Byte({self.value})"
    
class word:
    def __init__(self,value):
            if 0 <= value <= 65535:
                self.value = value
            else:
                raise ValueError("Word value must be between 0 and 65535")
            
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(int(self.value))
        elif target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Word'
    
    def __str__(self):
        return f"Word({self.value})"
    



class Int(Number):
    def __init__(self, value):
        self.value = int(value)
        
    def cast_to(self, target_type):
        if target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Int'
    
    def __str__(self):
        return f"Int({self.value})"
    
class Long(Int):
    def __init__(self, value):
        self.value = int(value)
        
    def cast_to(self, target_type):
        if target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Long'
    
    def __str__(self):
        return f"Long({self.value})"
    
class Short(Int):
    def __init__(self, value):
        if -32768 <= value <= 32767:
            self.value = int(value)
        else:
            raise ValueError("Short value must be between -32768 and 32767")
        
    def cast_to(self, target_type):
        if target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Short'
    
    def __str__(self):
        return f"Short({self.value})"

class Float(Number):
    def __init__(self, value):
        self.value = value
    
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(int(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Float'
    
    def __str__(self):
        return f"Float({self.value})"
    
    
class Double(Number):
    def __init__(self, value):
        self.value = value
    
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(int(self.value))
        elif target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Bool':
            return Bool(bool(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Double'
    
    def __str__(self):
        return f"Double({self.value})"
    
class Bool(Number):  #I think that is more convinient to have Bool as a subclass of Number
    def __init__(self, value):
        self.value = bool(value)
    
    def __and__(self, other):
        if isinstance(other, Bool):
            return Bool(self.value and other.value)
        raise TypeError(f"Cannot perform 'and' operation between {self.__class__.__name__} and {other.__class__.__name__}")
    
    def __or__(self, other):
        if isinstance(other, Bool):
            return Bool(self.value or other.value)
        raise TypeError(f"Cannot perform 'or' operation between {self.__class__.__name__} and {other.__class__.__name__}")
    
    def __not__(self):
        return Bool(not self.value)
    def __str__(self):
        return f"Bool({self.value})"
    
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(1 if self.value else 0)
        elif target_type == 'Float':
            return Float(1.0 if self.value else 0.0)
        elif target_type == 'Double':
            return Double(1.0 if self.value else 0.0)
        return self
    
    def __type__(self, env=None):
        return 'Bool'
    
class Char(BaseType):
    def __init__(self, value):
        if isinstance(value, str) and len(value) == 1:
            self.value = value
        else:
            raise ValueError("Char must be a single character string")
        
    def __str__(self):
        return f"Char('{self.value}')"
    
    def cast_to(self, target_type):
        pass 
    
    def __type__(self, env=None):
        return 'Char'

class String(BaseType):
    def __init__(self, value):
        if isinstance(value, str):
            self.value = value
        else:
            raise ValueError("String must be a string")
        
    def __str__(self):
        return f"String('{self.value}')"
    
    def cast_to(self, target_type):
        pass 

    def __type__(self, env=None):
        return 'String'
    

class unsigned_int(Int):
    def __init__(self, value):
        if value < 0:
            raise ValueError("Unsigned int cannot be negative")
        self.value = int(value)
    
    def __type__(self, env=None):
        return 'UnsignedInt'
    
    def __str__(self):
        return f"UnsignedInt({self.value})"
    
class unsigned_long(Long):
    def __init__(self, value):
        if value < 0:
            raise ValueError("Unsigned long cannot be negative")
        self.value = int(value)
    
    def __type__(self, env=None):
        return 'UnsignedLong'
    
    def __str__(self):
        return f"UnsignedLong({self.value})"
    
class unsigned_char(Char):
    def __init__(self, value):
        if isinstance(value, str) and len(value) == 1:
            self.value = value
        else:
            raise ValueError("Unsigned char must be a single character string")
        
    def __str__(self):
        return f"UnsignedChar('{self.value}')"
    
    def cast_to(self, target_type):
        pass 

    def __type__(self, env=None):
        return 'UnsignedChar'

class size_t(Int):
    def __init__(self, value):
        if value < 0:
            raise ValueError("size_t cannot be negative")
        self.value = int(value)
    
    def __type__(self, env=None):
        return 'size_t'
    
    def __str__(self):
        return f"size_t({self.value})"
    
class Object(BaseType):
    def __init__(self, value):
        self.name = value

    
    def __type__(self,env=None):
        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.name}' is not defined.")
        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.name}' is not defined.")
        return env.get_variable_type(self.name)
    
    def __str__(self):
        return f"Object({self.name})"
    
    def __name__(self):
        return self.name
    
    def execute(self, env):
        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.name}' is not defined.")
        contents = env.get_variable_contents(self.name)
        print(f"Executing Object: {self.name} with contents: {contents}")
        return env.get_variable_contents(self.name) 
    
#May be separated in another file
#-------------- Not basic types ---------------

class unary_operation(parserTypes):
    def __init__(self, operand, operation):
        self.operand = operand
        self.operation = operation
        self.children_list = [operand]
    
    def execute(self,env):
        return self.operand.unary_operation(self.operation)
    def __str__(self):
        return f"UnaryOperation({self.operand}, {self.operation})"


class binary_operation(parserTypes):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation
        self.children_list = [left, right]
    
    def execute(self,env):
        print(self.left)
        
        left_value = self.left.execute(env)
        right_value = self.right.execute(env)
        
        left_type = left_value.__type__()
        right_type = right_value.__type__()

        if left_type != right_type:
            type_hierarchy = {'Bool': 0, 'Int': 1, 'Float': 2, 'String': 3}
            left_rank = type_hierarchy.get(left_type, -1)
            right_rank = type_hierarchy.get(right_type, -1)
            print(f"Rank left:{left_rank}")
            print(f"Rank right:{right_rank}")

            print(f"Value left:{left_value}")
            print(f"Value right:{right_value}")

            if left_rank > right_rank:
                right_value = type_conversion(right_value,left_type)
            else:
                left_value = type_conversion(left_value,right_type)

        result = self.operation(left_value, right_value)
        print(f"Executing binary operation: {self.left} {self.operation.__name__} {self.right} = {result}")
        return result
    
    def __str__(self):
        return f"BinaryOperation({self.left}, {self.right}, {self.operation})"
    
    # This method return a string with the type
    def __type__(self, env=None):
        left_type = self.left.__type__(env).lower()
        right_type = self.right.__type__(env).lower()

        if left_type == right_type:
            return left_type
        
def type_conversion(object, target_type):
    original_type = object.__class__.__name__.lower() 
    target_type = target_type.lower()
    print(f"Original type: {original_type}, Target type: {target_type}")
    number_types = {"int", "float", "double", "bool"}
    if original_type == target_type:
        return object
    
    if original_type in number_types:
        if target_type == 'int':
            return Int(int(object.value))
        elif target_type == 'float':
            return Float(float(object.value))
        elif target_type == 'double':
            return Double(float(object.value))
        elif target_type == 'bool':
            return Bool(bool(object.value))
        
    if original_type == "string":
        if target_type == 'char':
            return Char(str(object.value)[0]) # This may be erroneous for c++ implementations
        
    if original_type == "char":
        if target_type == 'string':
            return String(str(object.value))

    
    raise RuntimeError(f"Cannot convert {original_type} to {target_type}. Only 'Object' type can be converted.")
    
def types_arduino_to_python(value):
        if value is None:
            return None
        
        if hasattr(value, 'value'):
            return value.value
        
        return value #This is if is already a Python Type
    
def python_to_types_arduino(value):
    if value in None:
        return None
        
    if isinstance(value, int):
        return Int(value)
    elif isinstance(value, float):
        return Float(value)
    elif isinstance(value, bool):
        return Bool(value)
    elif isinstance(value, str):
        return String(value)
    else:
        return value #This is if is already a TypeArduino Type

class assignment(parserTypes):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children_list = [name,value]
        
        
    def __type__(self, env=None):
        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.name}' is not defined.")
        
        var_type = env.get_variable_type(self.name)
        value_type = self.value.__type__(env)
        if var_type != value_type:
            raise RuntimeError(f"Type mismatch: cannot assign {value_type} to {var_type}.")
        return var_type
    
    def execute(self, env):


        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.name}' is not defined.")
        


        var_type = env.get_variable_type(self.name)
        execute_value = self.value.execute(env)
        converted_value = type_conversion(execute_value, var_type)
        env.modify_variable(self.name,converted_value)

    def __str__(self):
        return f"Assignment({self.name}, {self.value})"
    
#Auxiliary class to combine declarations
class declaration(parserTypes):
    def __init__(self, declaration):
        self.declaration = declaration
        self.children_list = [declaration]
        
    def execute(self, env):
        print(f"Executing declaration: {self.declaration}")
        declaration_types = ['simple_declaration', 'array_declaration', 'struct_declaration']
        if self.declaration.__class__.__name__ not in declaration_types:
            raise RuntimeError(f"Invalid declaration type: {self.declaration.__class__.__name__}. Expected one of {declaration_types}.")
        self.declaration.execute(env)
    
    def __str__(self):
        return f"Declaration({self.declaration})"
    
    def children(self):
        return self.children_list
    
    def __type__(self, env=None):
        return self.declaration.__type__(env)
    
class simple_declaration(parserTypes):
    def __init__(self,name,var_type, content=None):
        self.name = name
        self.var_type = var_type
        self.content = content
        self.children_list = [name, var_type, content] if content else [name, var_type]

    def __type__(self, env=None):
        return self.var_type
    
    def get_var_name(self, env=None):
        return self.name
    
    def var_content(self, env=None):
        if self.content is not None:
            return self.content.__type__(env)
        return None
    
    def change_content(self, content, env=None):
        self.content = content
        
        
        
    def execute(self, env):
        if self.content is not None:
            content = self.content.execute(env)
            content = type_conversion(content, self.var_type)
            env.set_variable(self.name, self.var_type, content)
        else:
            env.set_variable(self.name, self.var_type)
            
    def type_conversion(self,object, target_type):
        og_type = object.__class__.__name__.lower() # Original type of the object
        print(object)
        print(f"Original type: {og_type}, Target type: {target_type}")
        
        if og_type == target_type:
            return object
        print(f"Converting {object.__class__} to {target_type}")
        if og_type != 'Object':
            
            raise RuntimeError(f"Cannot convert {object.__class__.__name__} to {target_type}. Only 'Object' type can be converted.")
        
        if target_type == 'Int':
            return Int(int(object.name))
        elif target_type == 'Float':
            return Float(float(object.name))
        elif target_type == 'Double':
            return Double(float(object.name))
        elif target_type == 'Bool':
            return Bool(bool(object.name))
        elif target_type == 'Char':
            return Char(str(object.name)[0])
        elif target_type == 'String':
            return String(str(object.name))
        else:
            raise RuntimeError(f"Unsupported type conversion from {object.__class__.__name__} to {target_type}.")                     

            
    def __str__(self):
        return f"SimpleDeclaration(name={self.name}, type={self.var_type}, content={self.content})"
          
    def children(self):
        return self.children_list
          
class parenthesis(parserTypes):
    def __init__(self, expression):
        self.expression = expression
        self.children_list = [expression]

    def execute(self,env):
        return self.expression.execute(env)

    def __str__(self):
        return f"Parenthesis({self.expression})"

    def __type__(self, env=None):
        return self.expression.__type__(env)
    
    def children(self):
        return self.children_list

  
class program(parserTypes):
    def __init__(self,include_list,program_code_list):
        self.include_list = include_list
        self.program_code_list = program_code_list
        self.children_list = [include_list, program_code_list]
        
    def execute(self, env):
        # Antes de ejecutarlo self.program_code_list 
        for code in self.program_code_list.code_list: 
            if isinstance(code, function):
                if code.name == "setup": #Comprobar si es correcta la signature de setup
                    code.execute(env)
                elif code.name == "loop":
                    while True:
                            code.execute(env)

        # Execute includes first
        self.include_list.execute(env)
        # Then execute the program code
        self.program_code_list.execute(env)
    
    def children(self):
        return self.children_list
    
    def __str__(self):
        return f"Program(include_list={self.include_list}, program_code_list={self.program_code_list})"
    
class program_code_list(parserTypes):
    def __init__(self, code_list):
        self.code_list = code_list

    def execute(self, env):
        for code in self.code_list:
            code.execute(env)
            
    def __str__(self):
        return f"ProgramCodeList({len(self.code_list)} elements)"
    
    def append(self, code):
        print(f"Appending code: {code}")
        print(code)
        if not isinstance(code, program_code):
            raise RuntimeError(f"Expected a 'program_code' type, got {code.__class__.__name__}.")
        self.code_list.append(code)
        return self
    
    def children(self):
        return self.code_list



class program_code(parserTypes):
    def __init__(self, code):
        self.code = code
        self.children_list = [code]
    
    def execute(self, env):
        #Later we will add type checking and other features
        return self.code.execute(env)
    
    def __str__(self):
        return f"ProgramCode({self.code}), children: {len(self.children_list)} elements of types {[type(child).__name__ for child in self.children_list]}"
    

class sentence_list(parserTypes):
    def __init__(self, sentences):
        self.sentences = sentences
        self.children_list = sentences

    def execute(self, env):
        for sentence in self.sentences:
            sentence.execute(env)
        
    def __str__(self):
        return f"SentenceList({len(self.sentences)} sentences)"
    

    def append(self, sentence_item):
        if not isinstance(sentence_item, sentence):
            raise RuntimeError(f"Expected a 'sentence' type, got {sentence_item.__class__.__name__}.")
        self.sentences.append(sentence_item)
        self.children_list.append(sentence_item)
        return self


    

class sentence(parserTypes):
    def __init__(self, sentence):
        self.sentence = sentence
        self.children_list = [sentence]

    def execute(self, env):
        #Solo si el debugger esta activo, se checkea y se pausa, sino se ejecuta directamente
        if hasattr(env, 'debugger') and env.debugger:
            env.debugger.check_and_pause(self.lineno, env)
        return self.sentence.execute(env)
    
    def __str__(self):
        return f"Sentence({self.sentence})"

        
    
    
class include_list(parserTypes):
    def __init__(self, includes):
        self.includes = includes
        self.children_list = includes

    def execute(self, env):
        for include in self.includes:
            include.execute(env)
    
    def __str__(self):
        return "IncludeList"
    
    def children(self):
        return self.children_list
    
    def append(self, include_obj):
        if not isinstance(include_obj, include):
            raise RuntimeError(f"Expected an 'include' type, got {include.__class__.__name__}.")
        self.includes.append(include_obj)
        self.children_list.append(include_obj)
        return self


    def children(self):
        return  self.children_list


class include(parserTypes):
    def __init__(self, library_name):
        self.library_name = library_name.strip('"<>\'')
        if self.library_name.endswith('.h'):
            self.library_name = self.library_name[:-2]
        self.children_list = []

    def execute(self, env):
        try:
            if self.library_name == 'Serial':
                import libraries.serial as serial
                env.register_library('Serial', serial)
            elif self.library_name == 'Servo':
                import libraries.servo as servo
                env.register_library('Servo', servo)
            elif self.library_name == 'String':
                import libraries.string as string
                env.register_library('String', string)
            elif self.library_name == 'Keyboard':
                import libraries.keyboard as keyboard
                env.register_library('Keyboard', keyboard)
            else:
                print(f"Warning: Library '{self.library_name}' not found")
                return
            print(f"Library '{self.library_name}' registered successfully")
        except ImportError as e:
            print(f"Error importing library '{self.library_name}': {e}") 

    def __str__(self):
        return f"Include({self.library_name})"
    
    def __type__(self, env=None):
        return "Void"

#Control structures
class if_statement(parserTypes):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.children_list = [condition, body, else_body] if else_body else [condition, body]
        
    def execute(self, env):
        condition_result = self.condition.execute(env)
        if condition_result.__type__() != 'Bool':
            raise RuntimeError(f"Condition must be of type 'Bool', got {condition_result.__type__()}.")
        
        if condition_result.__value__():
            # Execute the body if the condition is true
            self.body.execute(env)
        elif self.else_body:
            # Execute the else body if the condition is false
            if self.else_body.__type__() is not None:
                self.else_body.execute(env)
                
    def __str__(self):
        return f"IfStatement(condition={self.condition}, body={self.body},else_body={self.else_body})"
    
#TODO: Add support for switch statements
class switch_statement(parserTypes):
    def __init__(self, expression, cases):
        self.expression = expression
        self.cases = cases 
        self.children_list = [expression, cases]

    def execute(self, env):
        evaluated_expression = self.expression.execute(env)
        if evaluated_expression.__type__() not in ['Int', 'String', 'Char']:
            raise RuntimeError(f"Switch expression must be of type 'Int', 'String' or 'Char', got {evaluated_expression.__type__()}.")
        
        self.cases.execute(env,evaluated_expression)
        
    pass

class case_sentence_list(parserTypes):
    def __init__(self, cases):
        self.cases = cases
        self.children_list = cases
        

    def execute(self, env, switch_expression):
        flag_break = False
        for case in self.cases:
            try:
                case.execute(env,switch_expression)
            except BreakException:
                break
            
        
            
    def __str__(self):
        return f"CaseList({len(self.cases)} cases)"
    
    def append(self, case_statement):
        if not isinstance(case_statement, case_sentence):
            raise RuntimeError(f"Expected a 'case_statement' type, got {case_statement.__class__.__name__}.")
        
        self.cases.append(case_statement)
        return self

class case_sentence(parserTypes):
    def __init__(self, expression, body):
        self.expression = expression
        self.body = body
        self.children_list = [expression, body]

    def execute(self, env, switch_expression):
        
        if self.expression is not None:
            evaluated_expression = self.expression.execute(env)
            if evaluated_expression.__type__() not in ['Int', 'String', 'Char']:
                raise RuntimeError(f"Case expression must be of type 'Int', 'String' or 'Char', got {evaluated_expression.__type__()}.")
        else:
            evaluated_expression = None
        
        if switch_expression.__str__() == evaluated_expression.__str__():
            self.body.execute(env)
        elif evaluated_expression is None:
            self.body.execute(env)
        



    def __str__(self):
        return f"CaseStatement(expression={self.expression}, body={self.body})"


class BreakException(Exception):
    pass


class break_statement(parserTypes):
    def __init__(self):
        self.children_list = []

    def execute(self, env):
        raise BreakException("Break triggered")
    
    def __str__(self):
        return "BreakStatement"


class for_loop(parserTypes):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body
        self.children_list = [init, condition, increment, body]
        if condition is None:
            self.condition = Bool(True)  # Default condition if not provided

    def execute(self, env):
        #Check types
        if self.condition.__type__() != 'Bool':
            raise RuntimeError(f"Condition must be of type 'Bool', got {self.condition.__type__()}.")
        
        if self.init.__class__.__name__ != 'assignment' and self.init is not None:
            raise RuntimeError(f"Initialization must be an assignment, got {self.init.__class__.__name__}.")

        if self.init.__type__(env) != 'Int' and self.init is not None: #This may be any number type, but for now we will use Int
            raise RuntimeError(f"Initialization must be of type 'Number', got {self.init.__type__(env)}.")
        
        # Execute the initialization
        if self.init is not None:
            self.init.execute(env)
        while True:
            # Check the loop condition
            condition_result = self.condition.execute(env)
            if condition_result.__type__() != 'Bool':
                raise RuntimeError(f"Condition must be of type 'Bool', got {condition_result.__type__()}.")

            if not condition_result.__value__():
                break

            # Execute the body
            self.body.execute(env)

            # Execute the increment
            self.increment.execute(env)
    
    def __str__(self):
        return f"ForLoop(init={self.init}, condition={self.condition}, increment={self.increment}, body={self.body})"
    

class while_loop(parserTypes):
    def __init__(self,expression,code):
        self.expression = expression
        self.code_block = code
        self.children = [self.expression,self.code_block]
        
    def execute(self,env):
        condition = self.expression.execute(env)
        condition.cast_to('Bool')
        if condition.__type__() != 'Bool':
            raise RuntimeError(f"Condition must be of type 'Bool', got {condition.__type__()}.")
        try:
            while condition.__value__():
                self.code_block.execute(env)
                condition = self.expression.execute(env)
                condition.cast_to('Bool')
                if condition.__type__() != 'Bool':
                    raise RuntimeError(f"Condition must be of type 'Bool', got {condition.__type__()}.")
        except BreakException:
            print("Break statement encountered, exiting while loop.")
        
class do_while_loop(parserTypes):
    def __init__(self, code_block, expression):
        self.code_block = code_block
        self.expression = expression
        self.children_list = [code_block, expression]
        
    def execute(self, env):
        try:
            while True:
                self.code_block.execute(env)
                condition = self.expression.execute(env)
                condition.cast_to('Bool')
                if condition.__type__() != 'Bool':
                    raise RuntimeError(f"Condition must be of type 'Bool', got {condition.__type__()}.")
                if not condition.__value__():
                    break
        except BreakException:
            print("Break statement encountered, exiting do-while loop.")
    
    def __str__(self):
        return f"DoWhileLoop(code_block={self.code_block}, expression={self.expression})"
    
#Functions and related classes
class void():
    def __init__(self):
        self.value = None

    def __type__():
        return "Void"
    



    

class function_args(parserTypes):
    def __init__(self,declarations):
        self.declarations = declarations
        self.children_list = declarations
        
    #It binds the arguments to the given enviroment
    def execute(self,env):
        for dec in self.declarations:
            dec.execute(env)
            
    #This method gives a string that are the types of the declaration separated by '#'
    def name_mangling(self):
        return '#'.join(str(decl.__type__()) for decl in self.declarations)
    
    def get_param_names(self):
        names = []
        for dec in self.declarations:
            names.append(dec.declaration.get_var_name())
        return names
    
    def get_param_types(self):
        types = []
        for dec in self.declarations:
            types.append(dec.declaration.__type__())
        return types
    
    def append(self,declaration_instance):
        if not isinstance(declaration_instance, declaration):
            raise RuntimeError(f"Expected a 'case_statement' type, got {declaration_instance.__class__.__name__}.")
        self.declarations.append(declaration_instance)
        return self
    
    def __str__(self):
        return f"FunctionArgs({self.declarations})"  
        
    

class function(parserTypes):
    def __init__(self, var_type, id, function_args, sentence_list):
        self.type = var_type
        self.function_name = id
        self.function_args = function_args
        self.function_body = sentence_list
        self.children_list = [function_args, sentence_list]
    
    def __type__(self):
        return self.type
    
    def name_mangling(self):
        if self.function_args is not None:
            types = self.function_args.get_param_types()
            return f"{self.function_name}#" + "#".join(types) + "#"
        else:
             return f"{self.function_name}#" #Dont now if I should mantain the las #

    def execute(self,env):
        env.set_function(self.name_mangling(), self)

    #This method creates a new enviroment for the function execution, it is used to implement the scope of the function
    def scope_generator(self,parent_env=None):
        new_scope = environment.Environment(parent_env)
        return new_scope
    
    #This method binds the arguments to the enviroment of the function
    def args_binding(self,list_of_arguments,env):
        param_names = self.function_args.get_param_names()
        param_types = self.function_args.get_param_types()
        for param_name, param_type, argument in zip(param_names, param_types, list_of_arguments):
            env.set_variable(param_name, param_type, argument)
            

    def body_execution(self,env):
        try:
            self.function_body.execute(env)
            if self.type.lower() != "void":
                raise RuntimeError("Expected return statement in function body.")
            
        except returnException as ret:
            ret_type = type(ret).__type__(ret).lower() if hasattr(ret, '__type__') else 'Void'
            print(f"Return type: {ret_type}, Expected type: {self.type}")
            if self.type.lower() != ret_type:
                converted_value = type_conversion(ret.value, self.type)
                return converted_value
            return ret.value
                

    
        
        
        
    def __str__(self):
        return f"Function(type={self.type}, name={self.function_name}, args={self.function_args}, body={self.function_body})"
    

class expression_list(parserTypes): #May need  to change the return to the type in data_structures
    def __init__(self,expressions):
        self.expressions = expressions

    def execute(self,env):
        result = []
        for expr in  self.expressions:
            result.append(expr.execute(env))
        return result
    
    def append(self,expr):
        self.expressions.append(expr)
        return self
    
    def __type__(self, env=None):
        types = []
        for expr in self.expressions:
            types.append(expr.__type__(env))
        return types



    def __str__(self):
        return f"ExpressionList({len(self.expressions)} expressions)"
    

        
 
class parameters(parserTypes):
    def __init__(self, expression_list):
        self.expression_list = expression_list

    def __type__(self,env=None):
        return self.expression_list.__type__(env)

    def execute(self,env):
        return self.expression_list.execute(env)
    

#Tramslates Arduino method names to Python method names
def arduino_to_python_name(lib_module, arduino_name: str) -> str:
    get_methods = getattr(lib_module, "get_methods", None)
    if callable(get_methods):
        spec = get_methods().get(arduino_name)
        if spec is not None:
            return spec[1]
    return arduino_name


class function_call(parserTypes):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
        
    def name_mangling(self, env = None):
        signature = f'{self.name}#'
        if self.parameters is not None:
            types = self.parameters.__type__(env)
            for t in types:
                signature += f"{t.lower()}#"
            return signature
        else:
            return signature

    def execute(self, env):
        args = self.parameters.execute(env) if self.parameters else []
        python_args = [types_arduino_to_python(arg) for arg in args]
        if '.' in self.name:
            lib_name, func_name = self.name.split('.')
            lib = env.libraries.get(lib_name)
            if lib is None:
                raise RuntimeError(f"Librería '{lib_name}' no encontrada. Usa #include")
            py_name = arduino_to_python_name(lib, func_name)
            if hasattr(lib, py_name):
                return getattr(lib, py_name)(*python_args)
            elif hasattr(lib, lib_name):  
                lib_class = getattr(lib, lib_name)
                instance = lib_class()
                if hasattr(instance, py_name):
                    return getattr(instance, py_name)(*python_args)
            raise RuntimeError(f"Método '{func_name}' no encontrado en librería '{lib_name}'")

        elif hasattr(env, 'built_in_functions') and self.name in env.built_in_functions:
            # Aquí pasamos los python_args ¡NO los args del AST!
            return env.built_in_functions[self.name](*python_args)
            
        else:
            signature = self.name_mangling(env)
            function_object = env.get_function(signature)
            new_env = function_object.scope_generator(env)
            

            if function_object.function_args is not None:
                function_object.args_binding(args, new_env)
                

            if hasattr(env, 'call_stack'):
                env.call_stack.append(self.name)
                
            try:
                result = function_object.body_execution(new_env)
                return result
            finally:
                if hasattr(env, 'call_stack'):
                    env.call_stack.pop()

class argument_list(parserTypes):
    def __init__(self, expressions):
        self.expressions = expressions
        
    def add_argument(self, expression):
        self.expressions.append(expression)
        return self
        
    def execute(self, env):
        return [expr.execute(env) for expr in self.expressions]
    
    def __type__(self,env):
        types = []
        for expr in self.expressions:
            types.append(expr.__type__(env))
        return types


class returnException(Exception):
    def __init__(self, value=void()):
        self.value = value
        
    def get_value(self):
        return self.value
    
    def __type__(self):
        if hasattr(self.value, '__type__'):
            return self.value.__type__()
        return "Void"
    

class return_statement(parserTypes):
    def __init__(self, expression):
        self.expression = expression
        self.children_list = [expression] if expression else []
        
    def execute(self, env):
        if self.expression is not None:
            value = self.expression.execute(env)
            raise returnException(value)
        else:
            raise returnException()
    
    def __str__(self):
        return f"ReturnStatement(expression={self.expression})"
    
    ##Estructuras de datos

class array_declaration(parserTypes):
    def __init__(self, name, element_type, size):
        self.name = name
        self.element_type = element_type
        self.size = size
        self.children_list = [name, element_type, size]

    def execute(self, env):
        env.set_variable(self.name, f"Array({self.element_type}, {self.size})", [None] * self.size)
    
    def __str__(self):
        return f"ArrayDeclaration(name={self.name}, element_type={self.element_type}, size={self.size})"
    
class array(parserTypes):
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.children_list = [name, index]

    def execute(self, env):
        array_info = env.get_variable_type(self.name)
        if not array_info.startswith("Array"):
            raise RuntimeError(f"Variable '{self.name}' is not an array.")
        
        element_type = array_info[array_info.find("(")+1:array_info.find(",")].strip()
        size = int(array_info[array_info.find(",")+1:array_info.find(")")].strip())
        
        index_value = self.index.execute(env)
        if index_value.__type__() != 'Int':
            raise RuntimeError(f"Array index must be of type 'Int', got {index_value.__type__()}.")
        
        if index_value.__value__() < 0 or index_value.__value__() >= size:
            raise RuntimeError(f"Array index out of bounds: {index_value.__value__()} for array of size {size}.")
        
        return env.get_variable_contents(self.name)[index_value.__value__()]
    
    def __str__(self):
        return f"Array(name={self.name}, index={self.index})"

if __name__ == "__main__":
    int1 = Int(5)
    int2 = Int(10)
    float1 = Float(5.5)
    op1sum = binary_operation(int1, float1, lambda a, b: a.__add__(b))
    print(op1sum.execute(environment.Environment()))  # Should print Int(15)
    
   
    
    