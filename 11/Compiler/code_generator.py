from parse_tree import *
from symbol_table import *
from code_map import *


class CodeGenerator:

    def __init__(self, parsed: JackClass, symbols: SymbolTable):
        self._class = parsed
        self._symbols = symbols
        self._cur_method = 'main'

    def vm(self):
        return merge(
            map(self.routine_vm, self._class.routines())
        )

    def routine_vm(self, routine: Subroutine):
        self._cur_method = routine.name()  # Side Effect!
        return merge(
            self.routine_header_vm(routine),
            self.routine_implied_vm(routine.modifier()),
            self.routine_body_vm(routine.body())
        )

    def routine_header_vm(self, routine: Subroutine):
        name = self.method_name(routine.name())
        nvar = self.variable_count(routine.body().local_variables())
        return function_declaration_vm(name, nvar)

    def routine_implied_vm(self, modifier):
        if modifier == 'constructor':
            return allocate_object_vm(self.class_size())
        elif modifier == 'method':
            return adjust_this_vm()
        else:
            return ''

    def routine_body_vm(self, body: RoutineBody):
        return self.statements_vm(body.statements())

    def class_size(self):
        var_dec = self._class.variables()
        fields = [dec for dec in var_dec if dec.modifier() == 'field']
        return self.variable_count(fields)

    def variable_count(self, var_dec):
        return sum([len(dec.names()) for dec in var_dec])

    def statements_vm(self, statements):
        return merge(
            map(self.statement_vm, statements)
        )

    def statement_vm(self, statement):
        if isinstance(statement, LetStatement):
            return self.let_vm(statement)
        elif isinstance(statement, IfStatement):
            return self.if_vm(statement)
        elif isinstance(statement, WhileStatement):
            return self.while_vm(statement)
        elif isinstance(statement, DoStatement):
            return self.do_vm(statement)
        elif isinstance(statement, ReturnStatement):
            return self.return_vm(statement)
        else:
            raise Exception('Illegal statement.')

    def let_vm(self, routine: LetStatement):
        return let_statement_vm(
            self.assignment_vm(routine.target()),
            self.expression_vm(routine.value())
        )

    def if_vm(self, routine: IfStatement):
        return if_statement_vm(
            self.expression_vm(routine.condition()),
            self.statements_vm(routine.consequent()),
            self.statements_vm(routine.alternative())
        )

    def while_vm(self, routine: WhileStatement):
        return while_statement_vm(
            self.expression_vm(routine.test()),
            self.statements_vm(routine.loop_body())
        )

    def do_vm(self, routine: DoStatement):
        return do_statement_vm(
            self.call_routine_vm(routine.routine_call())
        )

    def return_vm(self, routine: ReturnStatement):
        if not routine.value():
            return return_void_vm()
        return return_statement_vm(
            self.expression_vm(routine.value())
        )

    def assignment_vm(self, target):
        if isinstance(target, Variable):
            return assign_variable_vm(
                self.var_property(target.name())
            )
        else:
            return assign_array_entry_vm(
                self.var_property(target.name()),
                self.expression_vm(target.index())
            )

    def call_routine_vm(self, call):
        if isinstance(call, InClassCall):
            return inclass_call_vm(
                self.method_name(call.routine()),
                map(self.expression_vm, call.arguments())
            )
        else:
            return self.exclass_call_vm(call)

    def exclass_call_vm(self, call: ExClassCall):
        target = self.find_variable(call.target())
        if target:
            name = self.method_name(call.routine(), target.s_type())
            args = self.add_implicit_arg(call.target(), call.arguments())
        else:
            name = self.method_name(call.routine(), call.target())
            args = call.arguments()
        return routine_call(
            name,
            map(self.expression_vm, args)
        )

    def add_implicit_arg(self, name, arguments):
        first = Expression([Variable(name)])
        return [first] + arguments

    def expression_vm(self, exp: Expression):
        content = exp.content()
        ops = [i for i in content if isinstance(i, Operator)]
        terms = [i for i in content if not isinstance(i, Operator)]
        return merge(
            self.term_vm(terms[0]),
            self.rest_terms_vm(terms[1:], ops)
        )

    def rest_terms_vm(self, terms, ops):
        vm = []
        for term, op in zip(terms, ops):
            vm.append(self.term_vm(term))
            vm.append(binary_op_vm(op.value()))
        return merge(vm)

    def term_vm(self, term):
        if isinstance(term, IntegerConstant):
            return integer_vm(
                term.value()
            )
        elif isinstance(term, StringConstant):
            return string_vm(
                term.value()
            )
        elif isinstance(term, KeywordConstant):
            return keyword_vm(
                term.value()
            )
        elif isinstance(term, Variable):
            return variable_vm(
                self.var_property(term.name())
            )
        elif isinstance(term, ArrayEntry):
            return array_entry_vm(
                self.var_property(term.name()),
                self.expression_vm(term.index())
            )
        elif isinstance(term, UnaryTerm):
            return unary_vm(
                term.operator(),
                self.term_vm(term.term())
            )
        elif isinstance(term, Expression):
            return self.expression_vm(term)
        else:
            return self.call_routine_vm(term)

    def var_property(self, name):
        prop = self.find_variable(name)
        if prop:
            return prop.kind(), prop.index()
        else:
            raise Exception(f'{name} not defined.')

    def method_name(self, routine_name, class_name=None):
        if class_name:
            return f'{class_name}.{routine_name}'
        else:
            return f'{self._class.name()}.{routine_name}'

    def find_variable(self, name):
        symbols = self._symbols.method_symbols(self._cur_method)
        v_property = symbols.get(name)
        if v_property:
            return v_property
        symbols = self._symbols.class_symbols()
        v_property = symbols.get(name)
        if v_property:
            return v_property
        else:
            return None
