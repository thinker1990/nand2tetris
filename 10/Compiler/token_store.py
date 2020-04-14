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
        if word in SYMBOLS:
            self.tokens.append((T_TYPE.SYMBOL, word))
        elif word in KEYWORDS:
            self.tokens.append((T_TYPE.KEYWORD, word))
        elif word.isnumeric():
            self.tokens.append((T_TYPE.INT, int(word)))
        elif word.startswith('"') and word.endswith('"'):
            self.tokens.append((T_TYPE.STRING, word.strip('"')))
        else:
            self.tokens.append((T_TYPE.IDENTIFIER, word))

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

    def prepend_keyword(self, token):
        self.tokens.insert(0, (T_TYPE.KEYWORD, token))

    def prepend_symbol(self, token):
        self.tokens.insert(0, (T_TYPE.SYMBOL, token))

    def prepend_identifier(self, token):
        self.tokens.insert(0, (T_TYPE.IDENTIFIER, token))


class T_TYPE(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT = 3
    STRING = 4
