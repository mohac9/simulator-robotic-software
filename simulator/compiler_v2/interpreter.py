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
        if node.type == 'ASSIGNMENT':
            self.visitAssignmentStatement(node)
        elif node.type == 'PRINT':
            self.visitPrintStatement(node)
        elif node.type == 'IF':
            self.visitIfStatement(node)
        elif node.type == 'WHILE':
            self.visitWhileStatement(node)
        elif node.type == 'FOR':
            self.visitForStatement(node)
        elif node.type == 'BLOCK':
            self.visitBlockStatement(node)
        else:
            raise Exception(f"Unknown statement type: {node.type}")
    
    def printStatement(self, node):
        value = self.evaluate(node.expression)
        print(value)

    def assignmentStatement(self, node):
        name = node.name
        value = self.evaluate(node.expression)
        self.variables[name] = value
        return value
    
#TODO: Implementar la gestion de errores

       
   
    