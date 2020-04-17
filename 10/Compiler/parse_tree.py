class JackClass:

    def __init__(self, name, variables, routines):
        self._name = name
        self._vars = [*variables]
        self._routines = [*routines]

    def name(self):
        return self._name

    def variables(self):
        return self._vars

    def routines(self):
        return self._routines


class ClassVariable:

    def __init__(self, modifier, v_type, name):
        self._modifier = modifier
        self._type = v_type
        self._name = name

    def modifier(self):
        return self._modifier

    def v_type(self):
        return self._type

    def name(self):
        return self._name


class Subroutine:

    def __init__(self, modifier, r_type, name, parameters, body):
        self._modifier = modifier
        self._type = r_type
        self._name = name
        self._params = [*parameters]
        self._body = body

    def modifier(self):
        return self._modifier

    def return_type(self):
        return self._type

    def name(self):
        return self._name

    def parameters(self):
        return self._params

    def body(self):
        return self._body


class Parameter:

    def __init__(self, p_type, name):
        self._type = p_type
        self._name = name

    def param_type(self):
        return self._type

    def name(self):
        return self._name


class RoutineBody:

    def __init__(self, variables, statements):
        self._vars = [*variables]
        self._statements = [*statements]

    def local_variables(self):
        return self._vars

    def statements(self):
        return self._statements


class LocalVariable:

    def __init__(self, v_type, name):
        self._type = v_type
        self._name = name

    def v_type(self):
        return self._type

    def name(self):
        return self._name


class LetStatement:
    pass


class IfStatement:
    pass


class WhileStatement:
    pass


class DoStatement:
    pass


class ReturnStatement:
    pass


class Expression:
    pass
