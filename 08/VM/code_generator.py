from re import sub
from command import *
from code_map import *


class CodeGenerator:

    def __init__(self, vm_file):
        self.file = vm_file

    def generate(self, vm):
        asm_parts = map(self.assembly, vm)
        return self.format(self.merge(asm_parts))

    def assembly(self, cmd):
        if isinstance(cmd, Arithmetic):
            return arithmetic_asm(cmd.operation())
        elif isinstance(cmd, MemoryAccess):
            return self.memory_access_asm(cmd)
        elif isinstance(cmd, ProgramFlow):
            return self.program_flow_asm(cmd)
        else:
            raise(f'Undefined vm command: {cmd}')

    def merge(self, parts):
        return '\n'.join(parts)

    def format(self, asm):
        header = f'//{self.file}'
        compact = sub(r'[ \t]+', '', asm)
        return f'{header}\n{compact}'

    def memory_access_asm(self, cmd):
        if cmd.operation() == 'push':
            return push_asm(cmd.segment(), cmd.index(), self.file)
        else:
            return pop_asm(cmd.segment(), cmd.index(), self.file)

    def program_flow_asm(self, cmd):
        if cmd.operation() == 'label':
            return label_asm(cmd.label())
        elif cmd.operation() == 'goto':
            return goto_asm(cmd.label())
        else:
            return if_goto_asm(cmd.label())
