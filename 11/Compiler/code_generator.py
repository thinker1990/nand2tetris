from parse_tree import *
from symbol_table import *
from code_map import *


class CodeGenerator:

    def __init__(self, parsed: JackClass, symbols: SymbolTable):
        self._cname = parsed.name()
        self._size = self.class_size(parsed.variables())
        self._routines = parsed.routines()
        self._symbols = symbols
        self._cur_method = 'main'

    def class_size(self, var_dec):
        fields = [dec for dec in var_dec if dec.modifier() == 'field']
        return sum([len(dec.names()) for dec in fields])

    def vm(self):
        parts = []
        for routine in self._routines:
            self._cur_method = routine.name()
            parts.append(self.method_vm(routine))
        return join_strings(parts)

    def method_vm(self, routine: Subroutine):
        mname = self.method_name(routine.name())
        count = self.local_count(routine)
        return merge(
            function_dec_vm(mname, count),
            self.implicit_method_vm(routine.modifier()),
            self.statements_vm(routine.body().statements())
        )

    def implicit_method_vm(self, modifier):
        if modifier == 'constructor':
            return merge(
                constant_vm(self._size),
                call_vm('Memory.alloc', 1),
                pop_vm('pointer', 0)
            )
        elif modifier == 'method':
            return merge(
                push_vm('argument', 0),
                pop_vm('pointer', 0)
            )
        else:
            return ''

    def statements_vm(self, statements):
        return join_map(self.statement_vm, statements)

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
        return merge(
            self.expression_vm(routine.value()),
            self.assignment_vm(routine.target())
        )

    def if_vm(self, routine: IfStatement):
        else_label = unique_label('ELSE')
        done_label = unique_label('IF_DONE')
        return merge(
            self.not_cond(routine.condition()),
            if_goto_vm(else_label),
            self.statements_vm(routine.consequent()),
            goto_vm(done_label),
            label_vm(else_label),
            self.statements_vm(routine.alternative()),
            label_vm(done_label)
        )

    def while_vm(self, routine: WhileStatement):
        loop_label = unique_label('LOOP')
        done_label = unique_label('LOOP_DONE')
        return merge(
            label_vm(loop_label),
            self.not_cond(routine.test()),
            if_goto_vm(done_label),
            self.statements_vm(routine.loop_body()),
            goto_vm(loop_label),
            label_vm(done_label)
        )

    def do_vm(self, routine: DoStatement):
        return merge(
            self.call_routine_vm(routine.routine_call()),
            ignore_return_vm()
        )

    def return_vm(self, routine: ReturnStatement):
        if routine.value():
            return merge(
                self.expression_vm(routine.value()),
                'return'
            )
        else:
            return return_void_vm()

    def assignment_vm(self, target):
        if isinstance(target, Variable):
            return self.assign_var(target)
        else:
            return self.assign_array(target)

    def assign_var(self, target: Variable):
        seg, idx = self.destination(target.name())
        return pop_vm(seg, idx)

    def assign_array(self, target: ArrayEntry):
        seg, idx = self.destination(target.name())
        return merge(
            push_vm(seg, idx),
            self.expression_vm(target.index()),
            operator_vm('add'),
            pop_vm('pointer', 1),
            pop_vm('that', 0)
        )

    def destination(self, var_name):
        prop = self.find_var(var_name)
        if prop:
            return self.seg_idx(prop)
        else:
            raise Exception(f'{var_name} not defined.')

    def seg_idx(self, prop: SymbolProperty):
        kind, idx = prop.kind(), prop.index()
        if kind == 'static':
            return 'static', idx
        elif kind == 'field':
            return 'this', idx
        elif kind == 'argument':
            return 'argument', idx
        elif kind == 'var':
            return 'local', idx
        else:
            raise Exception(f'Illegal symbol kind {kind}')

    def not_cond(self, cond):
        return merge(
            self.expression_vm(cond),
            operator_vm('not')
        )

    def call_routine_vm(self, call):
        if isinstance(call, InClassCall):
            return self.inclass_call_vm(call)
        else:
            return self.exclass_call_vm(call)

    def inclass_call_vm(self, call: InClassCall):
        name = self.method_name(call.routine())
        narg = len(call.arguments()) + 1
        return merge(
            push_vm('pointer', 0),
            join_map(self.expression_vm, call.arguments()),
            call_vm(name, narg)
        )

    def exclass_call_vm(self, call: ExClassCall):
        target = self.find_var(call.target())
        if target:
            name = self.method_name(call.routine(), target.s_type())
            args = self.add_implicit_arg(call.target(), call.arguments())
        else:
            name = self.method_name(call.routine(), call.target())
            args = call.arguments()
        return merge(
            join_map(self.expression_vm, args),
            call_vm(name, len(args))
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
            vm.append(self.op_vm(op.value()))
        return join_strings(vm)

    def term_vm(self, term):
        if isinstance(term, IntegerConstant):
            return constant_vm(term.value())
        elif isinstance(term, StringConstant):
            return self.string_vm(term.value())
        elif isinstance(term, KeywordConstant):
            return self.keyword_vm(term.value())
        elif isinstance(term, Variable):
            return self.variable_vm(term.name())
        elif isinstance(term, ArrayEntry):
            return self.array_entry_vm(term.name(), term.index())
        elif isinstance(term, InClassCall):
            return self.inclass_call_vm(term)
        elif isinstance(term, ExClassCall):
            return self.exclass_call_vm(term)
        elif isinstance(term, Expression):
            return self.expression_vm(term)
        elif isinstance(term, UnaryTerm):
            return self.unary_vm(term.operator(), term.term())
        else:
            raise Exception('Illegal term type.')

    def string_vm(self, str_const):
        return merge(
            constant_vm(len(str_const)),
            call_vm('String.new', 1),
            join_map(self.append_char, str_const)
        )

    def append_char(self, char):
        return merge(
            constant_vm(ord(char)),
            call_vm('String.appendChar', 2)
        )

    def keyword_vm(self, word):
        if word in ('false', 'null'):
            return false_vm()
        elif word == 'true':
            return true_vm()
        else:
            return this_vm()

    def variable_vm(self, var):
        seg, idx = self.destination(var)
        return push_vm(seg, idx)

    def array_entry_vm(self, name, index):
        seg, idx = self.destination(name)
        return merge(
            push_vm(seg, idx),
            self.expression_vm(index),
            operator_vm('add'),
            pop_vm('pointer', 1),
            push_vm('that', 0)
        )

    def unary_vm(self, op, term):
        return merge(
            self.term_vm(term),
            self.unary_op(op)
        )

    def op_vm(self, operator):
        if operator == '+':
            return operator_vm('add')
        if operator == '-':
            return operator_vm('sub')
        if operator == '&':
            return operator_vm('and')
        if operator == '|':
            return operator_vm('or')
        if operator == '<':
            return operator_vm('lt')
        if operator == '>':
            return operator_vm('gt')
        if operator == '=':
            return operator_vm('eq')
        if operator == '*':
            return call_vm('Math.multiply', 2)
        if operator == '/':
            return call_vm('Math.divide', 2)

    def unary_op(self, operator):
        if operator == '-':
            return operator_vm('neg')
        if operator == '~':
            return operator_vm('not')

    def method_name(self, routine_name, class_name=None):
        if class_name:
            return f'{class_name}.{routine_name}'
        else:
            return f'{self._cname}.{routine_name}'

    def local_count(self, routine: Subroutine):
        decs = [dec for dec in routine.body().local_variables()]
        return sum([len(dec.names()) for dec in decs])

    def find_var(self, name):
        symbols = self._symbols.method_symbols(self._cur_method)
        prop = symbols.get(name)
        if prop:
            return prop
        symbols = self._symbols.class_symbols()
        prop = symbols.get(name)
        if prop:
            return prop
        else:
            return None


def join_map(action, iterator):
    return join_strings(map(action, iterator))


def join_strings(parts):
    return '\n'.join(parts)
