from code_map import DEST, JUMP, COMP
from command import A_Command, C_Command


class CodeGenerator:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def generate(self, asm):
        cmds = filter(self.translatable, asm)
        binary_parts = map(self.binary_code, cmds)
        return self.merge(binary_parts)

    def translatable(self, cmd):
        return isinstance(cmd, A_Command) or isinstance(cmd, C_Command)

    def binary_code(self, cmd):
        if isinstance(cmd, A_Command):
            return self.A_command_binary(cmd)
        else:
            return self.C_command_binary(cmd)

    def merge(self, parts):
        return '\n'.join(parts)

    def A_command_binary(self, cmd):
        symbol = cmd.symbol()
        if symbol.isnumeric():
            constant = int(symbol)
        else:
            constant = self.symbol_table.address_of(symbol)

        return f'0{self.binary_string(constant)}'

    def C_command_binary(self, cmd):
        dest_bin = DEST[cmd.dest()]
        comp_bin = COMP[cmd.comp()]
        jump_bin = JUMP[cmd.jump()]
        return f'111{comp_bin}{dest_bin}{jump_bin}'

    def binary_string(self, number):
        return '{:015b}'.format(number)
