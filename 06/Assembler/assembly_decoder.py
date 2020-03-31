from assembly_binary_map import DEST_TABLE, JUMP_TABLE, COMP_TABLE
from assembly_parser import A_Command, C_Command, L_Command


class AssemblyDecoder:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def generate_binary_code(self, parsed_asm):
        instructions = filter(self.is_instruction, parsed_asm)
        return [*map(self.binary_code_of, instructions)]

    def is_instruction(self, command):
        return not isinstance(command, L_Command)

    def binary_code_of(self, instruction):
        if isinstance(instruction, A_Command):
            return self.A_command_binary(instruction)
        else:
            return self.C_command_binary(instruction)

    def A_command_binary(self, instruction):
        symbol = instruction.symbol()
        if symbol.isnumeric():
            constant = int(symbol)
        else:
            constant = self.symbol_table.address_of(symbol)

        return f'0{self.dec_to_bin_str(constant)}\n'

    def C_command_binary(self, instruction):
        dest_bin = DEST_TABLE[instruction.dest()]
        comp_bin = COMP_TABLE[instruction.comp()]
        jump_bin = JUMP_TABLE[instruction.jump()]
        return f'111{comp_bin}{dest_bin}{jump_bin}\n'

    def dec_to_bin_str(self, number):
        return '{:015b}'.format(number)
