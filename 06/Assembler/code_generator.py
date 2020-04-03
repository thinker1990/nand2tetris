from code_map import DEST, JUMP, COMP
from command import A_Command, C_Command


class CodeGenerator:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def generate(self, parsed_asm):
        instructions = filter(self.is_instruction, parsed_asm)
        binary_parts = map(self.binary_code, instructions)
        return self.merge(binary_parts)

    def is_instruction(self, command):
        return isinstance(command, A_Command) or isinstance(command, C_Command)

    def binary_code(self, instruction):
        if isinstance(instruction, A_Command):
            return self.A_command_binary(instruction)
        else:
            return self.C_command_binary(instruction)

    def merge(self, parts):
        return '\n'.join(parts)

    def A_command_binary(self, instruction):
        symbol = instruction.symbol()
        if symbol.isnumeric():
            constant = int(symbol)
        else:
            constant = self.symbol_table.address_of(symbol)

        return f'0{self.binary_string(constant)}'

    def C_command_binary(self, instruction):
        dest_bin = DEST[instruction.dest()]
        comp_bin = COMP[instruction.comp()]
        jump_bin = JUMP[instruction.jump()]
        return f'111{comp_bin}{dest_bin}{jump_bin}'

    def binary_string(self, number):
        return '{:015b}'.format(number)
