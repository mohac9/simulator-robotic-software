import parser
import lexer

class interpreter:
    def __init__(self, code: str):
        self.code = code
        self.lexer = lexer.Lexer(code)
        self.parser = parser.Parser(self.lexer)
        self.variables = {}
        self.current_token = None
        self.current_node = None
        self.current_scope = None
        self.current_function = None
        
            
    def error(self, message: str):
        raise Exception(f"Error: {message}")
    
    def visitLiteral(self, node):
        return node.value
    
    #TODO 