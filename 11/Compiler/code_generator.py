from parse_tree import *
from symbol_table import *
from code_map import *


class CodeGenerator:

    def __init__(self, parsed: JackClass, symbols: SymbolTable):
        self._cname = parsed.name()
        self._routines = parsed.routines()
        self._symbols = symbols
        self._cur_method = 'main'

    def vm(self):
        parts = []
        for routine in self._routines:
            self._cur_method = routine.name()
            parts.append(self.method_vm(routine))
        return merge(parts)

    def method_vm(self, routine: Subroutine):
        mname = self.method_name(routine)
        count = self.argument_count(routine)
        return merge(
            function_dec_vm(mname, count),
            self.statements_vm(routine.body().statements())
        )

    def statements_vm(self, statements):
        slist = map(self.statement_vm, statements)
        return merge(slist)

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
            self.neg_cond(routine.condition()),
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
            self.neg_cond(routine.test()),
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
            return self.expression_vm(routine.value())
        else:
            return return_void_vm()

    def assignment_vm(self, target):
        if isinstance(target, Variable):
            return self.assign_var(target)
        else:
            return self.assign_array(target)

    def assign_var(self, target: Variable):
        pass

    def assign_array(self, target: ArrayEntry):
        pass

    def destination(self, var_name):
        symbols = self._symbols.method_symbols(self._cur_method)
        prop = symbols.get(var_name)
        if prop:
            return self.seg_idx(prop)
        symbols = self._symbols.class_symbols()
        prop = symbols.get(var_name)
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

    def neg_cond(self, cond):
        return merge(
            self.expression_vm(cond),
            operator_vm('neg')
        )

    def call_routine_vm(self, call):
        pass

    def expression_vm(self, exp):
        pass

    def method_name(self, routine: Subroutine):
        return f'{self._cname}.{routine.name()}'

    def argument_count(self, routine: Subroutine):
        if routine.modifier() == 'method':
            return 1 + len(routine.parameters())
        else:
            return len(routine.parameters())
