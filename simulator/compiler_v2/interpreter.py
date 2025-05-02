import parser
import lexer

class ArduinoInterpreter:
    def __init__(self, code):
        self.code = code
        self.variables = {}
        self.current_line = 0
        self.lines = []
        self.had_runtime_error = False

    #TODO
    def interpret(self,node):
        try:
            value = evaluate(node)
            print(value)
        except Exception as e:
            print(f"Error: {e}")
        


    #Retorna el valor de una variable
    def visitLiteralExpression(self, node):
       return node.value
   
    def visitGroupingExpression(self, node):
        return self.evaluate(node.expression)
    
    def evaluate(self,node):
        return node.accept(self)
    
    def visitUnaryExpression(self, node):
        right = self.evaluate(node.right)
        self.checkNumberOperand(node, right)
        if node.operator.type == 'MINUS':
            return -right
        else:
            return right
        
    def visitBinaryExpression(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        self.checkNumberOperands(node, left, right)
        
        if node.operator.type == 'PLUS':
            return left + right
        elif node.operator.type == 'MINUS':
            return left - right
        elif node.operator.type == 'MULTIPLY':
            return left * right
        elif node.operator.type == 'DIVIDE':
            return left / right
        elif node.operator.type == 'MODULUS':
            return left % right
        elif node.operator.type == 'AND':
            return left and right
        elif node.operator.type == 'OR':   
            return left or right
        elif node.operator.type == 'EQ':
            return left == right
        elif node.operator.type == 'NE':
            return left != right
        elif node.operator.type == 'LT':
            return left < right
        elif node.operator.type == 'LE':
            return left <= right
        elif node.operator.type == 'GT':
            return left > right
        elif node.operator.type == 'GE':
            return left >= right
        else:
            raise Exception(f"Unknown operator: {node.operator.type}")
        
    
    def checkNumberOperand(self, node, operand):
        if isinstance(operand, (int, float)):
            return True
        else:
            raise Exception(f"Operand must be a number: {operand}")
    
    def checkNumberOperands(self, node, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return True
        else:
            raise Exception(f"Operands must be numbers: {left}, {right}")
        
#Parte de los statement
    def statement(self, node):
        if node.type == 'assignment':
            self.visitAssignmentStatement(node)
        elif node.type == 'if':
            self.visitIfStatement(node)
        elif node.type == 'while':
            self.visitWhileStatement(node)
        elif node.type == 'do_while':
            self.visitDoWhileStatement(node)
        elif node.type == 'for':
            self.visitForStatement(node)
        elif node.type == 'BLOCK':
            self.visitBlockStatement(node)
        else:
            raise Exception(f"Unknown statement type: {node.type}")
    
    #El print se hace llamando a la GUI, no se hace en el interpreter
    

    def assignmentStatement(self, node):
        name = node.name
        value = self.evaluate(node.value)
        if name in self.variables:
            self.variables[name] = value
        else:
            raise Exception(f"Variable '{name}' not defined.")
        
    
    def visitIfStatement(self, node):
        condition = self.evaluate(node.condition)
        if condition:
            self.statement(node.then_branch)
        elif node.else_branch:
            self.statement(node.else_branch)

    def visitWhileStatement(self, node):
        while self.evaluate(node.expression):
            self.statement(node.sentence_list)

    def visitDoWhileStatement(self, node):
        while True:
            self.statement(node.sentence_list)
            if self.evaluate(node.expression):
                break
        
    def visitForStatement(self, node):
        for initializer in node.initializer:
            self.statement(initializer)
        while self.evaluate(node.condition):
            self.statement(node.sentence_list)
            for increment in node.increment:
                self.statement(increment)
   
    
    
#TODO: Implementar la gestion de errores

       
   
    