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
        elif isinstance(cmd, FunctionCall):
            return self.function_call_asm(cmd)
        else:
            raise(f'Undefined vm command: {cmd}')

    @classmethod
    def bootstrap(cls):
        return cls.trim_space(bootstrap_code())

    def merge(self, parts):
        return '\n'.join(parts)

    def format(self, asm):
        header = f'//{self.file}'
        body = self.trim_space(asm)
        return f'{header}\n{body}'

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

    def function_call_asm(self, cmd):
        if cmd.operation() == 'function':
            return function_asm(cmd.func_name(), cmd.arg_count())
        elif cmd.operation() == 'call':
            return call_asm(cmd.func_name(), cmd.arg_count())
        else:
            return return_asm()

    @classmethod
    def trim_space(cls, text):
        return sub(r'[ \t]+', '', text)
