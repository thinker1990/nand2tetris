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
        while self.tokens.peek() in ('let', 'if', 'while', 'do', 'return'):
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
        key = self.tokens.peek()
        if key == 'let':
            return self.let_statement()
        elif key == 'if':
            return self.if_statement()
        elif key == 'while':
            return self.while_statement()
        elif key == 'do':
            return self.do_statement()
        elif key == 'return':
            return self.return_statement()
        else:
            raise 'Illegal statement.'

    def let_statement(self):
        s_type = self.tokens.pop_keyword()
        variable = self.tokens.pop_identifier()
        if self.tokens.peek() == '[':
            self.tokens.pop_symbol()  # [
            index = self.expression()
            self.tokens.pop_symbol()  # ]
        self.tokens.pop_symbol()
        value = self.expression()
        self.tokens.pop_symbol()
        return s_type, variable, index, value

    def if_statement(self):
        s_type = self.tokens.pop_keyword()
        self.tokens.pop_symbol()  # (
        cond = self.expression()
        self.tokens.pop_symbol()  # )
        self.tokens.pop_symbol()  # {
        consequent = self.statements()
        self.tokens.pop_symbol()  # }
        if self.tokens.peek() == 'else':
            self.tokens.pop_keyword()
            self.tokens.pop_symbol()  # {
            alternative = self.statements()
            self.tokens.pop_symbol()  # }
        return s_type, cond, consequent, alternative

    def while_statement(self):
        s_type = self.tokens.pop_keyword()
        self.tokens.pop_symbol()  # (
        cond = self.expression()
        self.tokens.pop_symbol()  # )
        self.tokens.pop_symbol()  # {
        consequent = self.statements()
        self.tokens.pop_symbol()  # }
        return s_type, cond, consequent

    def do_statement(self):
        s_type = self.tokens.pop_keyword()
        r_call = self.routine_call()
        self.tokens.pop_symbol()
        return s_type, r_call

    def return_statement(self):
        s_type = self.tokens.pop_keyword()
        if self.tokens.peek() == ';':
            self.tokens.pop_symbol()
            return s_type, None
        else:
            exp = self.expression()
            self.tokens.pop_symbol()
            return s_type, exp

    def routine_call(self):
        first = self.tokens.pop()
        second = self.tokens.pop()
        self.tokens.prepend(second)
        self.tokens.prepend(first)
        if second == '.':
            return self.indirect_call()
        else:
            return self.direct_call()

    def direct_call(self):
        routine = self.tokens.pop_identifier()
        self.tokens.pop_symbol()  # (
        arguments = self.expression_list()
        self.tokens.pop_symbol()  # )
        return routine, arguments

    def indirect_call(self):
        target = self.tokens.pop_identifier()
        self.tokens.pop_symbol()
        call = self.direct_call()
        return target, call

    def expression_list(self):
        pass

    def expression(self):
        pass
