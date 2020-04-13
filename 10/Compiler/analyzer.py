
class Analyzer:

    def __init__(self, tokens):
        self.tokens = [*tokens]

    def parse_tree(self):
        return self.tokens  # TODO

    def parse_class(self, tokens):
        name = ''
        variabls = self.class_vars(tokens)
        routines = self.subroutines(tokens)
        return name, variabls, routines

    def class_vars(self, tokens):
        while True:
            yield self.class_var(tokens)

    def subroutines(self, tokens):
        while True:
            yield self.subroutine(tokens)

    def class_var(tokens):
        var_type = None
        name = ''
        return var_type, name

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
