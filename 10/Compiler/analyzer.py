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
        while self.tokens.peek() in ('static', 'field'):
            yield self.variable()

    def subroutines(self):
        while self.tokens.peek() in ('constructor', 'function', 'method'):
            yield self.subroutine()

    def subroutine(self):
        modifier = self.tokens.pop_keyword()
        r_type = self.tokens.pop()
        name = self.tokens.pop_identifier()
        self.tokens.pop_symbol()  # (
        params = self.parameters()
        self.tokens.pop_symbol()  # )
        body = self.routine_body()
        return modifier, r_type, name, params, body

    def parameters(self):
        while self.tokens.peek() != ')':
            yield self.parameter()

    def parameter(self):
        if self.tokens.peek() == ',':
            self.tokens.pop()
        p_type = self.tokens.pop()
        name = self.tokens.pop_identifier()
        return p_type, name

    def routine_body(self):
        self.tokens.pop_symbol()  # {
        variables = self.local_vars()
        statements = self.statements()
        self.tokens.pop_symbol()  # }
        return variables, statements

    def local_vars(self):
        while self.tokens.peek() == 'var':
            yield self.variable()

    def statements(self):
        while self.tokens.peek() != '}':
            yield self.statement()

    def variable(self):
        modifier = self.tokens.pop_keyword()
        v_type = self.tokens.pop()  # keyword | identifier
        name = self.tokens.pop_identifier()
        if self.tokens.pop_symbol() == ',':
            self.prepare_next_var(modifier, v_type)
        return modifier, v_type, name

    def prepare_next_var(self, modifier, v_type):
        self.tokens.prepend(v_type)
        self.tokens.prepend(modifier)

    def statement(self):
        pass
