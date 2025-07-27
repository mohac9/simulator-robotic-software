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
    
    def __str__(self):
        return f"Int({self.value})"

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
    
    
class Object(BaseType):
    def __init__(self, value):
        self.name = value

    
    def __type__(self,env=None):
        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.name}' is not defined.")
        return env[self.name]
    
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
        
        result = self.operation(left_value, right_value)
        print(f"Executing binary operation: {self.left} {self.operation.__name__} {self.right} = {result}")
        return result
    
    def __str__(self):
        return f"BinaryOperation({self.left}, {self.right}, {self.operation})"
    
    # This method return a string with the type
    def __type__(self, env=None):
        left_type = self.left.__type__()
        right_type = self.right.__type__()

        if left_type == right_type:
            return left_type
        
def type_conversion(object, target_type):
    original_type = object.__class__.__name__.lower() 
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
    


class assignment(parserTypes):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children_list = [name,value]
        
        
    def __type__(self, env=None):
        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.variable}' is not defined.")
        
        var_type = env.get_variable_type(self.name)
        value_type = self.value.__type__(env)
        if var_type != value_type:
            raise RuntimeError(f"Type mismatch: cannot assign {value_type} to {var_type}.")
        return var_type
    
    def execute(self, env):


        if self.name not in env.variables:
            raise RuntimeError(f"Variable '{self.variable}' is not defined.")
        


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
    
    def __var_name__(self, env=None):
        return self.name
    
    def __var_content__(self, env=None):
        if self.content is not None:
            return self.content.__type__(env)
        return None
    
    def __change_content__(self, content, env=None):
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
        return str(self.code)
    

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
    
    def append(self, include):
        if not isinstance(include, include):
            raise RuntimeError(f"Expected an 'include' type, got {include.__class__.__name__}.")
        self.includes.append(include)
        self.children_list.append(include)
        return self

class include(parserTypes):
    def __init__(self, include_name):
        self.include_name = include_name
        self.children_list  = [include_name]
    def execute(self, env):
        if self.include_name.__type__(env) != 'String':
            raise RuntimeError(f"Include name must be a string, got {self.include_name.__type__(env)}.")
        #TODO: Implement include functionality
    def children(self):
        return  self.children_list

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
    

#Functions and related classes

class function():
    def __init__(self, var_type, id, function_args, sentence_list):
        self.type = var_type
        self.funtion_name = id
        self.function_args = function_args
        self.function_body = sentence_list
        self.children = [sentence_list]
    
    def __type__(self):
        return self.type

    def execute(self,env):
        #TODO:Create a new env for the function

        #TODO:Enter the function_args into variables in the env

        #TODO:Execut the sentence_list with the new env

        #TODO:Return an expresion if type is not null
        pass
    



if __name__ == "__main__":
    int1 = Int(5)
    int2 = Int(10)
    float1 = Float(5.5)
    op1sum = binary_operation(int1, float1, lambda a, b: a.__add__(b))
    print(op1sum.execute(environment.Environment()))  # Should print Int(15)
    
   
    
    