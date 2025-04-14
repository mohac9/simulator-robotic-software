# coding: utf-8

from sly import Lexer
import os
import re
import sys

def comentario(t):
    if t.value.startswith('/*'):
        t.type = 'BLOCK_COMMENT'
        return t
    elif t.value.startswith('//'):
        t.type = 'LINE_COMMENT'
        return t
    else:
        return t
    
    
class ArduinoLexer(Lexer):
    literals = {'(', ')', '{', '}', '[', ']', ';', ',', '.', '=', '+', '-', '*', '/', '%', '!', '<', '>', '&', '|', '^', '~'}
    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'//.*|/\*.*?\*/'
    keywords = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'for': 'FOR',
        'return': 'RETURN',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'void': 'VOID',
        'int': 'INT',
        'float': 'FLOAT',
        'char': 'CHAR',
        'bool': 'BOOL',
        'true': 'TRUE',
        'false': 'FALSE',
    }
    tokens = { 'ID', 'NUMBER', 'STRING', 'CHAR', 'CHAR_CONST', 'BOOL_CONST' } | set(keywords.values())
    pass


    @_(r'//.*')
    def LINE_COMMENT(self, t):
        pass
    
    @_(r'/\*.*?\*/')
    def BLOCK_COMMENT(self, t):
        pass
    
    @_(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
    def ID(self, t):
        t.type = self.keywords.get(t.value, 'ID')
        return t
    
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = t.value[1:-1]  # Remove quotes
        return t
    
    @_(r'\'[^\']\'')
    def CHAR_CONST(self, t):
        t.value = t.value[1:-1]  # Remove quotes
        return t
    
    @_(r'\b(true|false)\b')
    def BOOL_CONST(self, t):
        t.value = t.value == 'true'
        return t
    
    @_(r'\s+')
    def WHITESPACE(self, t):
        pass
    
    @_(r'\n')
    def NEWLINE(self, t):
        self.lineno += 1
        self.index = 0
        pass
    
    @_(r'[\(\)\{\}\[\];,\.=\+\-\*\/\%\!\<\>\&\|\^\~]')
    def SYMBOL(self, t):
        return t
    
    
    


if __name__ == '__main__':
    data = '''
    int main() {
        // This is a line comment
        /* This is a block comment */
        int x = 10;
        float y = 20.5;
        char z = 'a';
        bool flag = true;
        if (x < y) {
            x = x + 1;
        }
        return 0;
    }
    '''
    
    lexer = ArduinoLexer()
    for token in lexer.tokenize(data):
        print(token)