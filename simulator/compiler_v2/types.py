
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

class Float(Number):
    def __init__(self, value):
        self.value = value
    
    def cast_to(self, target_type):
        if target_type == 'Int':
            return Int(int(self.value))
        elif target_type == 'Double':
            return Double(float(self.value))
        return self
    
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
    
class Char(BaseType):
    def __init__(self, value):
        if isinstance(value, str) and len(value) == 1:
            self.value = value
        else:
            raise ValueError("Char must be a single character string")
        
    def __str__(self):
        return f"Char('{self.value}')"
    
    def cast_to(self, target_type):
        pass #I have to ask Domingo how I DRY it

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




if __name__ == "__main__":
    int1 = Int(5)
    int2 = Int(10)
    float1 = Float(5.5)
    double1 = Double(10.5)
    bool1 = Bool(True)
    
    print(int1 + int2)  # Should print Number(15)
    print(float1 + double1)  # Should print Float(16.0)
    print(bool1 and Bool(False))  # Should print Bool(False)
    
    print(int1.cast_to('Float'))  # Should print Float(5.0)
    print(float1.cast_to('Int'))  # Should print Int(5)
