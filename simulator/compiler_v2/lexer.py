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
        'switch': 'SWITCH',
        'case': 'CASE',
        'default': 'DEFAULT',
        'LOW': 'LOW',
        'HIGH': 'HIGH',
        'ANALOG_PIN': 'ANALOG_PIN',
        'INPUT': 'INPUT',
        'INPUT_PULLUP': 'INPUT_PULLUP',
        'OUTPUT': 'OUTPUT',
        'HEX_CONST': 'HEX_CONST',
        'OCTAL_CONST': 'OCTAL_CONST',
        'BINARY_CONST': 'BINARY_CONST',
        'INT_CONST': 'INT_CONST',
        'FLOAT_CONST': 'FLOAT_CONST',
        'CHAR_CONST': 'CHAR_CONST',
        'STRING_CONST': 'STRING_CONST',
        'ID': 'ID'
        
    }
    tokens = { 'ID', 'NUMBER', 'STRING', 'CHAR', 'CHAR_CONST', 'BOOL_CONST','EQUAL','SEMICOLON', 'NOT_EQUAL','INCLUDE', 'STRING_CONST', 'CONST', 'STATIC',
              'LBRACKET', 'RBRACKET','LBRACE', 'RBRACE','COMMA','DEFINE','LPAREN','RPAREN','BREAK','RETURN',
              'CONTINUE', 'WHILE','DO','FOR','CASE','COLON','DEFAULT','IF','SWITCH','ELSE'
              ,'AND','OR','NOT','EQ','NE','LT','LE','GT','GE','PLUS','MINUS','MULTIPLY','DIVIDE','MODULUS',
              'BITWISE_AND','BITWISE_OR','BITWISE_XOR','BITWISE_NOT','BITWISE_LEFT_SHIFT','BITWISE_RIGHT_SHIFT',
              'UNSIGNED_INT','SIGNED_INT','FLOAT','DOUBLE','LONG','SHORT','BYTE','WORD','UNSIGNED_LONG','UNSIGNED_CHAR',
              'SIZE_T','BOOLEAN'
              } | set(keywords.values())
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
    
    

    @_(r'\,')
    def COMMA(self, t):
        return t
    
    @_(r'\#define')
    def DEFINE(self, t):
        return t
    
    @_(r'\bbreak\b')
    def BREAK(self, t):
        return t
    
    @_(r'\breturn\b')
    def RETURN(self, t):
        return t
    
    @_(r'\bcontinue\b')
    def CONTINUE(self, t):
        return t
    
    @_(r'\bwhile\b')
    def WHILE(self, t):
        return t
    
    @_(r'\bdo\b')
    def DO(self, t):
        return t
    
    @_(r'\bfor\b')
    def FOR(self, t):
        return t
    
    @_(r'\bcase\b')
    def CASE(self, t):
        return t
    
    @_(r'\:')
    def COLON(self, t):
        return t
    
    @_(r'\bdefault\b')
    def DEFAULT(self, t):
        return t
    
    @_(r'\bswitch\b')
    def SWITCH(self, t):
        return t
    
    @_(r'\bif\b')
    def IF(self, t):
        return t
    
    @_(r'\belse\b')
    def ELSE(self, t):
        return t
    
    @_(r'\&\&')
    def AND(self, t):
        return t
    
    @_(r'\|\|')
    def OR(self, t):
        return t
    
    @_(r'\!')
    def NOT(self, t):
        return t
    
    @_(r'\=\=')
    def EQ(self, t):
        return t
    
    @_(r'\!\=')
    def NE(self, t):
        return t
    
    @_(r'\<')
    def LT(self, t):
        return t
    
    @_(r'\<=')
    def LE(self, t):
        return t
    
    @_(r'\>')
    def GT(self, t):
        return t
    
    @_(r'\>=')
    def GE(self, t):
        return t
    
    @_(r'\+')
    def PLUS(self, t):
        return t
    
    @_(r'\-')
    def MINUS(self, t):
        return t
    
    @_(r'\*')
    def MULTIPLY(self, t):
        return t
    
    @_(r'\/')
    def DIVIDE(self, t):
        return t
    
    @_(r'\%')
    def MODULUS(self, t):
        return t
    
    @_(r'\&')
    def BITWISE_AND(self, t):
        return t
    
    @_(r'\|')
    def BITWISE_OR(self, t):
        return t
    
    @_(r'\^')
    def BITWISE_XOR(self, t):
        return t
    
    @_(r'\~')
    def BITWISE_NOT(self, t):
        return t
    
    @_(r'\<\<')
    def BITWISE_LEFT_SHIFT(self, t):
        return t
    
    @_(r'\>\>')
    def BITWISE_RIGHT_SHIFT(self, t):
        return t
    
    @_(r'\bunsigned\b')
    def UNSIGNED_INT(self, t):
        return t
    
    @_(r'\bsigned\b')
    def SIGNED_INT(self, t):
        return t
    
    @_(r'\bfloat\b')
    def FLOAT(self, t):
        return t
    
    @_(r'\bdouble\b')
    def DOUBLE(self, t):
        return t
    
    @_(r'\blong\b')
    def LONG(self, t):
        return t
    
    @_(r'\bshort\b')
    def SHORT(self, t):
        return t
    
    @_(r'\bbyte\b')
    def BYTE(self, t):
        return t
    
    @_(r'\bword\b')
    def WORD(self, t):
        return t
    
    @_(r'\bint\b')
    def INT(self, t):
        return t
    
    @_(r'\bunsigned long\b')
    def UNSIGNED_LONG(self, t):
        return t
    
    @_(r'\bunsigned char\b')
    def UNSIGNED_CHAR(self, t):
        return t
    
    @_(r'\bsize_t\b')
    def SIZE_T(self, t):
        return t
    
    @_(r'\bboolean\b')
    def BOOLEAN(self, t):
        return t
    

  

    
    @_(r'[\(\)\{\}\[\];,\.=\+\-\*\/\%\!\<\>\&\|\^\~]')
    def SYMBOL(self, t):
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
    a + b;
    }
    '''
    
    lexer = ArduinoLexer()
    for token in lexer.tokenize(data):
        print(token)