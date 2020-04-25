from parse_tree import *
from symbol_table import *


class CodeGenerator:

    def __init__(self, parsed: JackClass, symbols: SymbolTable):
        self._routines = parsed.routines()
        self._csymbols = symbols.class_symbols()

    def vm(self):
        pass
