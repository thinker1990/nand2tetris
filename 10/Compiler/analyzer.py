from token_store import TokenStore


class Analyzer:

    def __init__(self, tokens: TokenStore):
        self.tokens = tokens.clone()

    def parse_tree(self):
        return self.parse_class()

    def parse_class(self):
        keyword = self.tokens.pop_keyword()
        if keyword != 'class':
            raise 'keyword "class" expected'
        name = self.class_name()
        self.tokens.pop_symbol()  # {
        variabls = self.class_vars()
        routines = self.subroutines()
        self.tokens.pop_symbol()  # }
        return name, variabls, routines

    def class_name(self):
        return self.tokens.pop_identifier()

    def class_vars(self):
        token = self.tokens.peek()
        while token in ('static', 'field'):
            yield self.class_var()
            token = self.tokens.peek()

    def subroutines(self):
        token = self.tokens.peek()
        while token in ('constructor', 'function', 'method'):
            yield self.subroutine()
            token = self.tokens.peek()

    def class_var(self):
        modifier = self.tokens.pop_keyword()
        v_type = self.tokens.pop()  # keyword | identifier
        name = self.tokens.pop_identifier()
        if self.tokens.pop_symbol() == ',':
            self.prepare_next_var(modifier, v_type)
        return modifier, v_type, name

    def prepare_next_var(self, modifier, v_type):
        if v_type in ('int', 'char', 'boolean'):
            self.tokens.prepend_keyword(v_type)
        else:
            self.tokens.prepend_identifier(v_type)
        self.tokens.prepend_keyword(modifier)

    def subroutine(self):
        pass
