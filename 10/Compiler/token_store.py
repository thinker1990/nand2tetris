from enum import Enum
from terminal import *


class TokenStore:

    def __init__(self):
        self.tokens = []

    def clone(self):
        copy = TokenStore()
        copy.tokens = self.tokens.copy()
        return copy

    def push(self, word):
        t_type = token_type(word)
        self.tokens.append((t_type, word))

    def prepend(self, word):
        t_type = token_type(word)
        self.tokens.insert(0, (t_type, word))

    def peek(self, index=0):
        _, token = self.tokens[index]
        return token

    def pop(self):
        _, token = self.tokens.pop(0)
        return token

    def pop_keyword(self):
        return self.pop_token(T_TYPE.KEYWORD)

    def pop_symbol(self):
        return self.pop_token(T_TYPE.SYMBOL)

    def pop_identifier(self):
        return self.pop_token(T_TYPE.IDENTIFIER)

    def pop_int(self):
        num = self.pop_token(T_TYPE.INT)
        return int(num)

    def pop_string(self):
        string = self.pop_token(T_TYPE.STRING)
        return string.strip('"')

    def pop_token(self, token_type):
        t_type, token = self.tokens.pop(0)
        if t_type == token_type:
            return token
        else:
            self.tokens.insert(0, (t_type, token))
            raise Exception(f'{token_type} excepted.')


class T_TYPE(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT = 3
    STRING = 4


def token_type(word):
    if word in SYMBOLS:
        return T_TYPE.SYMBOL
    elif word in KEYWORDS:
        return T_TYPE.KEYWORD
    elif word.isnumeric():
        return T_TYPE.INT
    elif word.startswith('"') and word.endswith('"'):
        return T_TYPE.STRING
    else:
        return T_TYPE.IDENTIFIER
