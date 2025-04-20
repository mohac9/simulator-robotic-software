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
    tokens = { 'ID', 'NUMBER', 'STRING', 'CHAR', 'CHAR_CONST', 'BOOL_CONST','EQUAL','SEMICOLON', 'NOT_EQUAL','INCLUDE', 'STRING_CONST', 'CONST', 'STATIC',
              'LBRACKET', 'RBRACKET','LBRACE', 'RBRACE','COMMA','DEFINE','LPAREN','RPAREN'} | set(keywords.values())
    pass

    def __init__(self):
        self.include = False # Esta para diferenciar entre el string_const y el string

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
    
    @_(r'\".*?\"|<.*?>')
    def STRING_CONST(self, t):
        if self.include:
            self.include = False
            t.value = t.value[1:-1]
            return t
        else:
            self.error(t)
    
    @_(r'\".*?\"')
    def STRING(self, t):
        if not self.include:
            t.value = t.value[1:-1]
            return t
        else:
            self.error(t)
    
    @_(r'\'[^\']\'')
    def CHAR_CONST(self, t):
        t.value = t.value[1:-1]  
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
    
    @_(r'=')
    def EQUAL(self, t):
        return t
    
    @_(r'!=')
    def NOT_EQUAL(self, t):
        return t
    
    @_(r';')
    def SEMICOLON(self, t):
        return t
    
    @_(r'#include')
    def INCLUDE(self, t):
        self.include = True
        return t
    
    @_(r'\bconst\b')
    def CONST(self, t):
        return t
    
    @_(r'\bstatic\b')
    def STATIC(self, t):
        return t
    
    @_(r'\[')
    def LBRACKET(self, t):
        return t
    
    @_(r'\]')
    def RBRACKET(self, t):
        return t
    
    @_(r'\{')
    def LBRACE(self, t):
        return t
    
    @_(r'\}')
    def RBRACE(self, t):
        return t
    
    @_(r'\(')
    def LPAREN(self, t):
        return t
    
    @_(r'\)')
    def RPAREN(self, t):
        return t
    
    @_(r'[\(\)\{\}\[\];,\.=\+\-\*\/\%\!\<\>\&\|\^\~]')
    def SYMBOL(self, t):
        return t

    @_(r'\,')
    def COMMA(self, t):
        return t
    
    @_(r'\#define')
    def DEFINE(self, t):
        return t
    
    
    
    def salida(self,t):
        Lexer = ArduinoLexer()
        list_strings = []
        for token in Lexer.tokenize(t):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'CHAR_CONST':
                result += f"'{token.value}'"
            else:
                result += f"{token.value}"
            list_strings.append(result)
        return list_strings
    
    


if __name__ == '__main__':
    data = '''
    #include <Arduino.h>
    
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