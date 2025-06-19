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
    
    
    
    


class BaseType(metaclass=Metatype):
    
    
    def __add__(self, other):
        return NotImplemented
    
    def __str__(self):
        return self.__class__.__name__ # for debugging purposes
    

class parserTypes:
    def __init__(self):
        self.children = []
        
    def children(self):
        return self.children
    
    
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
        return self.binary_operation(other, lambda a, b: Number(a.value + b.value))
    def __sub__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value - b.value))
    def __mul__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value * b.value))
    def __truediv__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value / b.value))
    def __floordiv__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value // b.value))
    def __mod__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value % b.value))
    def __pow__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value ** b.value))
    def __neg__(self):
        return Number(-self.value)
    
    # Arithmetic unary operators

    def __abs__(self):
        return Number(abs(self.value))
    
    def __prev__(self):
        return Number(self.value - 1)
    
    def __next__(self):
        return Number(self.value + 1)
    

    # Bitwise operators
    def __bit_shift_r__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value >> b.value))
    def __bit_shift_l__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value << b.value))
    
    def __bitwise_and__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value & b.value))
    def __bitwise_or__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value | b.value))
    def __bitwise_xor__(self, other):
        return self.binary_operation(other, lambda a, b: Number(a.value ^ b.value))
    
    def __bitwise__not__(self):
        return Number(~self.value)
    
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

class Int(Number):
    def __init__(self, value):
        self.value = int(value)
        
    def cast_to(self, target_type):
        if target_type == 'Float':
            return Float(float(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        return self
    
    def __type__(self, env=None):
        return 'Int'

class Float(Number):
    def __init__(self, value):
        self.value = value
    
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(int(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
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
#May be separated in another file
#-------------- Not basic types ---------------

class unary_operation(parserTypes):
    def __init__(self, operand, operation):
        self.operand = operand
        self.operation = operation
        self.children = [operand]
    
    def execute(self):
        return self.operand.unary_operation(self.operation)
    def __str__(self):
        return f"UnaryOperation({self.operand}, {self.operation})"


class binary_operation(parserTypes):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation
        self.children = [left, right]
    
    def execute(self):
        return self.left.binary_operation(self.right, self.operation)
    
    def __str__(self):
        return f"BinaryOperation({self.left}, {self.right}, {self.operation})"
    
    # This method return a string with the type
    def __type__(self, env=None):
        left_type = self.left.__type__()
        right_type = self.right.__type__()

        if left_type == right_type:
            return left_type
        


class assignment(parserTypes):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
        self.children = [variable,value]
        
    def __type__(self, env=None):
        if self.variable not in env.variables:
            raise RuntimeError(f"Variable '{self.variable}' is not defined.")
        var_type = env.get_variable_type(self.variable)
        value_type = self.value.__type__(env)
        if var_type != value_type:
            raise RuntimeError(f"Type mismatch: cannot assign {value_type} to {var_type}.")
        return var_type
    
    
    
    def execute(self, env):
        if self.variable not in env.variables:
            raise RuntimeError(f"Variable '{self.variable}' is not defined.")
        
        var_type = env.get_variable_type(self.variable)
        value_type = self.value.__type__(env)

        if var_type != value_type:
            raise RuntimeError(f"Type mismatch: cannot assign {value_type} to {var_type}.")
        
        env.modify_variable(self.variable, self.value)

    def __str__(self):
        return f"Assignment({self.variable}, {self.value})"
    
class simple_declaration:
    def __init__(self,name,var_type, content=None):
        self.name = name
        self.var_type = var_type
        self.content = content
        
    def __type__(self, env=None):
        return self.var_type
    
    def __var_name__(self, env=None):
        return self.name
    
    def __var_content__(self, env=None):
        if self.content is not None:
            return self.content.__type__(env)
        return None
    
    def __change_content__(self, content, env=None):
        self.content = content
        
        
    def execute(self, env):
        env.set_variable(self.name, self.var_type)
        if self.content is not None:
            content_type = self.content.__type__(env)
            if content_type != self.var_type:
                raise RuntimeError(f"Type mismatch: cannot assign {content_type} to {self.var_type}.")
            env.set_variable_contents(self.name, self.content)
            
    def __str__(self):
        return f"SimpleDeclaration(name={self.name}, type={self.var_type}, content={self.content})"
          
          
class parenthesis(parserTypes):
    def __init__(self, expression):
        self.expression = expression
        self.children = [expression]

    def execute(self):
        return self.expression.execute()

    def __str__(self):
        return f"Parenthesis({self.expression})"

    def __type__(self, env=None):
        return self.expression.__type__(env)

  
class program(parserTypes):
    def __init__(self,include_list,program_code):
        self.include_list = include_list
        self.program_code = program_code
        
    def execute(self, env):
        pass

class Object():
    def __init__(self, value):
        self.name = value

    
    def __type__(self,env=None):

        return env[self.name]
    
    
#Control structures
class if_statement(parserTypes):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.children = [condition, body, else_body] if else_body else [condition, body]
        
    def execute(self, env):
        condition_result = self.condition.execute()
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


class for_loop(parserTypes):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body
        self.children = [init, condition, increment, body]

    def execute(self, env):
        #Check types
        if self.condition.__type__() != 'Bool':
            raise RuntimeError(f"Condition must be of type 'Bool', got {self.condition.__type__()}.")
        
        if self.init.__class__.__name__ != 'assignment':
            raise RuntimeError(f"Initialization must be an assignment, got {self.init.__class__.__name__}.")

        if self.init.__type__(env) != 'Int': #This may be any number type, but for now we will use Int
            raise RuntimeError(f"Initialization must be of type 'Number', got {self.init.__type__(env)}.")
        
        # Execute the initialization
        self.init.execute(env)
        while True:
            # Check the loop condition
            condition_result = self.condition.execute()
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



if __name__ == "__main__":
    int1 = Int(5)
    int2 = Int(10)
    float1 = Float(5.5)
    double1 = Double(10.5)
    bool1 = Bool(True)
    bool2 = bool1.__not__()
    print(bool1, bool2)
    
   
    # Example usage of binary_operation using Int's __add__ method
    op = binary_operation(int1, float1, Number.__add__)
    result = op.execute()
    print(result)