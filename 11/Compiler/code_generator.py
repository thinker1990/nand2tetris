from parse_tree import *
from symbol_table import *
from code_map import *


class CodeGenerator:

    def __init__(self, parsed: JackClass, symbols: SymbolTable):
        self._cname = parsed.name()
        self._routines = parsed.routines()
        self._csymbols = symbols.class_symbols()

    def vm(self):
        parts = map(self.method_vm, self._routines)
        return self.merge(parts)

    def method_vm(self, routine: Subroutine):
        mname = self.method_name(routine)
        count = self.argument_count(routine)
        head = function_vm(mname, count)
        body = map(self.statement_vm, routine.body().statements())
        return self.merge([head] + [*body])

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
        pass

    def if_vm(self, routine: IfStatement):
        pass

    def while_vm(self, routine: WhileStatement):
        pass

    def do_vm(self, routine: DoStatement):
        pass

    def return_vm(self, routine: ReturnStatement):
        pass

    def method_name(self, routine: Subroutine):
        return f'{self._cname}.{routine.name()}'

    def argument_count(self, routine: Subroutine):
        if routine.modifier() == 'method':
            return 1 + len(routine.parameters())
        else:
            return len(routine.parameters())

    def merge(self, parts):
        return '\n'.join(parts)
