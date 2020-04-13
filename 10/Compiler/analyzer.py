from terminal import *


class Analyzer:

    def __init__(self, tokens):
        self.tokens = [*tokens]

    def parse_tree(self):
        return self.parse_class()

    def parse_class(self):
        keyword = self.pop_head(TOKEN_TYPE.KEYWORD)
        if keyword != 'class':
            raise 'keyword "class" expected'
        name = self.class_name()
        variabls = self.class_vars()
        routines = self.subroutines()
        return name, variabls, routines

    def class_name(self):
        return self.pop_head(TOKEN_TYPE.IDENTIFIER)

    def next_token(self, token_type):
        t_type, token = self.tokens[0]
        if t_type == token_type:
            return token
        else:
            raise 'mismatched token type'

    def pop_head(self, token_type):
        token = self.next_token(token_type)
        self.tokens.pop(0)
        return token

    def class_vars(self):
        self.unpack_class()
        keyword = self.next_token(TOKEN_TYPE.KEYWORD)
        while keyword in ('static', 'field'):
            yield self.class_var()
            keyword = self.next_token(TOKEN_TYPE.KEYWORD)

    def unpack_class(self):
        self.pop_head(TOKEN_TYPE.SYMBOL)
        self.tokens.pop()

    def class_var(self):
        modifier = self.pop_head(TOKEN_TYPE.KEYWORD)
        try:
            v_type = self.pop_head(TOKEN_TYPE.KEYWORD)
        except:
            v_type = self.pop_head(TOKEN_TYPE.IDENTIFIER)
        name = self.pop_head(TOKEN_TYPE.IDENTIFIER)
        if self.pop_head(TOKEN_TYPE.SYMBOL) == ',':
            self.tokens.
        return modifier, v_type, name

    def subroutine(tokens):
        name = ''
        params = self.parameters(tokens)
        body = self.routine_body(tokens)
        return name, params, body

    def parameters():
        while True:
            yield self.parameter()

    def routine_body():
        variables = self.local_vars()
        statements = self.statements()
        return variables, statements

    def parameter():
        p_type = None
        p_name = ''
        return p_type, p_name

    def local_vars():
        while True:
            yield self.local_var()

    def statements():
        while True:
            yield self.statement()

    def local_var():
        l_type = None
        l_name = ''
        return l_type, l_name

    def statement():
        pass
