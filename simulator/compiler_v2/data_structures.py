'''
This module defines the data structures used in c++
'''

class BaseDataStructure:
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"
    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
    
class Struct(BaseDataStructure):
    def __init__(self, name: str, fields: dict):
        super().__init__(name)
        self.fields = fields  # fields is a dictionary of field names and their types

    def __repr__(self):
        return f"Struct({self.name}, fields={self.fields})"

    def __str__(self):
        return f"Struct({self.name}, fields={self.fields})"
    
class Array(BaseDataStructure):
    def __init__(self, name: str, element_type: str, size: int):
        super().__init__(name)
        self.element_type = element_type
        self.size = size

    def __repr__(self):
        return f"Array({self.name}, element_type={self.element_type}, size={self.size})"

    def __str__(self):
        return f"Array({self.name}, element_type={self.element_type}, size={self.size})"