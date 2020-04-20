class JackClass:

    def __init__(self, name, variables, routines):
        self._name = name
        self._vars = variables
        self._routines = routines

    def name(self):
        return self._name

    def variables(self):
        return self._vars

    def routines(self):
        return self._routines


class ClassVariable:

    def __init__(self, modifier, v_type, names):
        self._modifier = modifier
        self._type = v_type
        self._names = names

    def modifier(self):
        return self._modifier

    def v_type(self):
        return self._type

    def names(self):
        return self._names


class Subroutine:

    def __init__(self, modifier, r_type, name, parameters, body):
        self._modifier = modifier
        self._type = r_type
        self._name = name
        self._params = parameters
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
        self._vars = variables
        self._statements = statements

    def local_variables(self):
        return self._vars

    def statements(self):
        return self._statements


class LocalVariable:

    def __init__(self, v_type, names):
        self._type = v_type
        self._names = names

    def v_type(self):
        return self._type

    def names(self):
        return self._names


class LetStatement:

    def __init__(self, target, value):
        self._target = target
        self._value = value

    def target(self):
        return self._target

    def value(self):
        return self._value


class IfStatement:

    def __init__(self, condition, consequent, alternative):
        self._cond = condition
        self._consq = consequent
        self._alter = alternative

    def condition(self):
        return self._cond

    def consequent(self):
        return self._consq

    def alternative(self):
        return self._alter


class WhileStatement:

    def __init__(self, test, loop):
        self._test = test
        self._loop = loop

    def test(self):
        return self._test

    def loop_body(self):
        return self._loop


class DoStatement:

    def __init__(self, routine_call):
        self._call = routine_call

    def routine_call(self):
        return self._call


class ReturnStatement:

    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value


class Expression:

    def __init__(self, terms):
        self._terms = terms

    def content(self):
        return self._terms


class Operator:

    def __init__(self, op):
        if op not in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            raise f'Illegal operator: {op}.'
        self._op = op

    def value(self):
        return self._op


class InClassCall:

    def __init__(self, routine, arguments):
        self._routine = routine
        self._args = arguments

    def routine(self):
        return self._routine

    def arguments(self):
        return self._args


class ExClassCall:

    def __init__(self, target, routine, arguments):
        self._target = target
        self._routine = routine
        self._args = arguments

    def target(self):
        return self._target

    def routine(self):
        return self._routine

    def arguments(self):
        return self._args


class IntegerConstant:

    def __init__(self, value):
        if not isinstance(value, int):
            raise Exception('Integer constant expected')
        self._value = value

    def value(self):
        return self._value


class StringConstant:

    def __init__(self, value):
        if not isinstance(value, str):
            raise Exception('String constant expected')
        self._value = value

    def value(self):
        return self._value


class KeywordConstant:

    def __init__(self, value):
        if value not in ('true', 'false', 'null', 'this'):
            raise f'Illegal keyword: {value}.'
        self._value = value

    def value(self):
        return self._value


class Variable:

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name


class ArrayEntry:

    def __init__(self, name, index):
        self._name = name
        self._index = index

    def name(self):
        return self._name

    def index(self):
        return self._index


class UnaryTerm:

    def __init__(self, operator, term):
        if operator not in ('-', '~'):
            raise f'Illegal unary operator: {operator}.'
        self._op = operator
        self._term = term

    def operator(self):
        return self._op

    def term(self):
        return self._term
