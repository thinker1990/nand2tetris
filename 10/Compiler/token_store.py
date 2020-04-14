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
        self.tokens.append(self.token(word))

    def prepend(self, word):
        self.tokens.insert(0, self.token(word))

    def token(self, word):
        if word in SYMBOLS:
            return T_TYPE.SYMBOL, word
        elif word in KEYWORDS:
            return T_TYPE.KEYWORD, word
        elif word.isnumeric():
            return T_TYPE.INT, word
        elif word.startswith('"') and word.endswith('"'):
            return T_TYPE.STRING, word
        else:
            return T_TYPE.IDENTIFIER, word

    def peek(self):
        _, token = self.tokens[0]
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

    def pop_token(self, token_type):
        t_type, token = self.tokens.pop(0)
        if t_type == token_type:
            return token
        else:
            self.tokens.insert(0, (t_type, token))
            raise f'{token_type} excepted.'


class T_TYPE(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT = 3
    STRING = 4
