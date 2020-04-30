from parse_tree import *
from symbol_table import *
from code_map import *


class CodeGenerator:

    def __init__(self, parsed: JackClass):
        self._class = parsed
        self._symbols = SymbolTable()

    def vm(self):
        # Side Effect!
        self._symbols.add_class_symbols(self._class)
        return merge(
            lmap(self.routine_vm, self._class.routines())
        )

    def routine_vm(self, routine: Subroutine):
        # Side Effect!
        self._symbols.add_method_symbols(routine)
        return merge(
            self.routine_header_vm(routine),
            self.routine_implied_vm(routine.modifier()),
            self.routine_body_vm(routine.body())
        )

    def routine_header_vm(self, routine: Subroutine):
        return method_declaration_vm(
            method_name(routine.name(), self._class.name()),
            self._symbols.method_var_count()
        )

    def routine_implied_vm(self, modifier):
        if modifier == 'constructor':
            size = self._symbols.class_instance_size()
            return allocate_object_vm(size)
        elif modifier == 'method':
            return adjust_this_vm()
        else:
            return ''

    def routine_body_vm(self, body: RoutineBody):
        return self.statements_vm(body.statements())

    def statements_vm(self, statements):
        return merge(
            lmap(self.statement_vm, statements)
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
                self._symbols.where_is(target.name())
            )
        else:
            return assign_array_entry_vm(
                self._symbols.where_is(target.name()),
                self.expression_vm(target.index())
            )

    def call_routine_vm(self, call):
        if isinstance(call, InClassCall):
            return call_inclass_vm(
                method_name(call.routine(), self._class.name()),
                lmap(self.expression_vm, call.arguments())
            )
        else:
            return self.exclass_call_vm(call)

    def exclass_call_vm(self, call: ExClassCall):
        if self._symbols.defined(call.target()):
            target_type = self._symbols.type_of(call.target())
            return call_instance_vm(
                self._symbols.where_is(call.target()),
                method_name(call.routine(), target_type),
                lmap(self.expression_vm, call.arguments())
            )
        else:
            return call_static_vm(
                method_name(call.routine(), call.target()),
                lmap(self.expression_vm, call.arguments())
            )

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
            return integer_vm(term.value())
        elif isinstance(term, StringConstant):
            return string_vm(term.value())
        elif isinstance(term, KeywordConstant):
            return keyword_vm(term.value())
        elif isinstance(term, Variable):
            return variable_vm(
                self._symbols.where_is(term.name())
            )
        elif isinstance(term, ArrayEntry):
            return array_entry_vm(
                self._symbols.where_is(term.name()),
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


def lmap(func, iterable):
    return list(map(func, iterable))
