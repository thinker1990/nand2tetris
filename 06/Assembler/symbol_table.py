from predefined_symbols import PREDEFINED_SYMBOLS
from command import A_Command, L_Command


class SymbolTableBuilder:

    _INSTRUCTION_START_ADDRESS = 0
    _VARIABLE_START_ADDRESS = 16

    def __init__(self):
        self.table = PREDEFINED_SYMBOLS.copy()

    def build(self, asm):
        self.add_labels(asm)
        self.add_variables(asm)
        return SymbolTable(self.table)

    def add_labels(self, asm):
        address = self._INSTRUCTION_START_ADDRESS
        for cmd in asm:
            if isinstance(cmd, L_Command):
                self.table[cmd.label()] = address
            else:
                address += 1

    def add_variables(self, asm):
        address = self._VARIABLE_START_ADDRESS
        for cmd in filter(self.non_constant, asm):
            if not cmd.symbol() in self.table:
                self.table[cmd.symbol()] = address
                address += 1

    def non_constant(self, cmd):
        return isinstance(cmd, A_Command) and not cmd.symbol().isnumeric()


class SymbolTable():

    def __init__(self, symbol_table: dict):
        self.symbol_table = symbol_table.copy()

    def address_of(self, symbol: str):
        return self.symbol_table[symbol]
