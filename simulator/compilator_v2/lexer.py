import re

class ArduinoLexer:
    def __init__(self):
        self.tokens = []
        self.keywords = {
            "void", "int", "float", "char", "if", "else", "for", "while", "return", 
            "digitalWrite", "digitalRead", "analogWrite", "analogRead", "pinMode", "delay"
        }
        self.token_specification = [
            ('NUMBER', r'\b\d+(\.\d+)?\b'),  # Integer or decimal number
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identifiers
            ('OPERATOR', r'[+\-*/=<>!&|]+'),  # Operators
            ('DELIMITER', r'[(),;{}]'),  # Delimiters
            ('STRING', r'"[^"]*"'),  # String literals
            ('NEWLINE', r'\n'),  # Line endings
            ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
            ('MISMATCH', r'.'),  # Any other character
        ]
        self.token_regex = re.compile('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specification))

    def tokenize(self, code):
        for match in self.token_regex.finditer(code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'IDENTIFIER' and value in self.keywords:
                kind = 'KEYWORD'
            elif kind == 'SKIP' or kind == 'NEWLINE':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {value}')
            self.tokens.append((kind, value))
        return self.tokens

