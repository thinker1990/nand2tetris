from token_store import *
from parse_tree import *


class Analyzer:

    def __init__(self, tokens: TokenStore):
        self.tokens = tokens.clone()

    def parse_tree(self):
        return self.parse_class()

    def parse_class(self):
        keyword = self.tokens.pop_keyword()
        if keyword != 'class':
            raise Exception('Jack class expected')
        name = self.class_name()
        self.tokens.pop_symbol()  # {
        variabls = self.class_vars()
        routines = self.subroutines()
        self.tokens.pop_symbol()  # }
        return JackClass(name, variabls, routines)

    def class_name(self):
        return self.tokens.pop_identifier()

    def class_vars(self):
        result = []
        while self.tokens.peek() in ('static', 'field'):
            result.append(self.class_var())
        return result

    def subroutines(self):
        result = []
        while self.tokens.peek() in ('constructor', 'function', 'method'):
            result.append(self.subroutine())
        return result

    def class_var(self):
        modifier, v_type, names = self.var_dec()
        return ClassVariable(modifier, v_type, names)

    def subroutine(self):
        modifier = self.tokens.pop_keyword()
        r_type = self.tokens.pop()
        name = self.tokens.pop_identifier()
        self.tokens.pop_symbol()  # (
        params = self.parameters()
        self.tokens.pop_symbol()  # )
        body = self.routine_body()
        return Subroutine(modifier, r_type, name, params, body)

    def parameters(self):
        result = []
        while self.tokens.peek() != ')':
            result.append(self.parameter())
        return result

    def routine_body(self):
        self.tokens.pop_symbol()  # {
        variables = self.local_vars()
        statements = self.statements()
        self.tokens.pop_symbol()  # }
        return RoutineBody(variables, statements)

    def parameter(self):
        p_type = self.tokens.pop()
        name = self.tokens.pop_identifier()
        if self.tokens.peek() == ',':
            self.tokens.pop()
        return Parameter(p_type, name)

    def local_vars(self):
        result = []
        while self.tokens.peek() == 'var':
            result.append(self.local_var())
        return result

    def statements(self):
        result = []
        while self.tokens.peek() in ('let', 'if', 'while', 'do', 'return'):
            result.append(self.statement())
        return result

    def local_var(self):
        _, v_type, names = self.var_dec()
        return LocalVariable(v_type, names)

    def var_dec(self):
        modifier = self.tokens.pop_keyword()
        v_type = self.tokens.pop()  # keyword | identifier
        names = [self.tokens.pop_identifier()]
        while self.tokens.pop_symbol() != ';':
            names.append(self.tokens.pop_identifier())
        return modifier, v_type, names

    # statement

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
            raise Exception('Illegal statement.')

    def let_statement(self):
        self.tokens.pop_keyword()
        target = self.let_target()
        self.tokens.pop_symbol()
        value = self.expression()
        self.tokens.pop_symbol()
        return LetStatement(target, value)

    def let_target(self):
        if self.tokens.peek(1) == '[':
            return self.array_entry()
        else:
            return self.var_name()

    def if_statement(self):
        self.tokens.pop_keyword()
        cond = self.exp_in_parenthesis()
        consequent = self.statements_in_braces()
        alternative = self.if_alternative()
        return IfStatement(cond, consequent, alternative)

    def if_alternative(self):
        if self.tokens.peek() == 'else':
            self.tokens.pop_keyword()
            return self.statements_in_braces()
        else:
            return []

    def while_statement(self):
        self.tokens.pop_keyword()
        test = self.exp_in_parenthesis()
        loop = self.statements_in_braces()
        return WhileStatement(test, loop)

    def do_statement(self):
        self.tokens.pop_keyword()
        r_call = self.routine_call()
        self.tokens.pop_symbol()
        return DoStatement(r_call)

    def return_statement(self):
        self.tokens.pop_keyword()
        if self.tokens.peek() == ';':
            value = None
        else:
            value = self.expression()
        self.tokens.pop_symbol()
        return ReturnStatement(value)

    def routine_call(self):
        if self.tokens.peek(1) == '.':
            return self.exclass_call()
        else:
            return self.inclass_call()

    def inclass_call(self):
        routine, arguments = self.call()
        return InClassCall(routine, arguments)

    def exclass_call(self):
        target = self.tokens.pop_identifier()
        self.tokens.pop_symbol()
        routine, arguments = self.call()
        return ExClassCall(target, routine, arguments)

    def call(self):
        routine = self.tokens.pop_identifier()
        self.tokens.pop_symbol()  # (
        arguments = self.argument_list()
        self.tokens.pop_symbol()  # )
        return routine, arguments

    def argument_list(self):
        result = []
        while not self.expression_end():
            result.append(self.argument())
        return result

    def argument(self):
        arg = self.expression()
        if self.tokens.peek() == ',':
            self.tokens.pop()
        return arg

    def exp_in_parenthesis(self):
        self.tokens.pop_symbol()  # (
        exp = self.expression()
        self.tokens.pop_symbol()  # )
        return exp

    def statements_in_braces(self):
        self.tokens.pop_symbol()  # {
        statements = self.statements()
        self.tokens.pop_symbol()  # }
        return statements

    # expression

    def expression(self):
        first = self.term()
        rest = self.op_terms()
        return Expression([first] + rest)

    def op_terms(self):
        result = []
        while not self.expression_end():
            result.append(self.operator())
            result.append(self.term())
        return result

    def expression_end(self):
        return self.tokens.peek() in (')', ']', ';', ',')

    def operator(self):
        return Operator(self.tokens.pop_symbol())

    def term(self):
        first = self.tokens.peek()
        if token_type(first) == T_TYPE.INT:
            return self.int_const()
        elif token_type(first) == T_TYPE.STRING:
            return self.str_const()
        elif token_type(first) == T_TYPE.KEYWORD:
            return self.keyword()
        elif first == '(':
            return self.exp_in_parenthesis()
        elif first in ('-', '~'):
            return self.unary_term()
        elif token_type(first) == T_TYPE.IDENTIFIER:
            return self.complex_term()
        else:
            raise Exception(f'Illegal term start with: {first}.')

    def int_const(self):
        return IntegerConstant(self.tokens.pop_int())

    def str_const(self):
        return StringConstant(self.tokens.pop_string())

    def keyword(self):
        return KeywordConstant(self.tokens.pop_keyword())

    def unary_term(self):
        op = self.tokens.pop_symbol()
        term = self.term()
        return UnaryTerm(op, term)

    def complex_term(self):
        op = self.tokens.peek(1)
        if op == '[':
            return self.array_entry()
        elif op in ('(', '.'):
            return self.routine_call()
        else:
            return self.var_name()

    def var_name(self):
        return Variable(self.tokens.pop_identifier())

    def array_entry(self):
        array = self.tokens.pop_identifier()
        self.tokens.pop_symbol()  # [
        index = self.expression()
        self.tokens.pop_symbol()  # ]
        return ArrayEntry(array, index)
