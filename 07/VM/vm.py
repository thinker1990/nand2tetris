from re import sub
from arithmetic import Arithmetic
from memory_access import MemoryAccess
import constants as const


class VM:

    def __init__(self, file_name):
        self.file = file_name

    def translate(self, vm_text):
        lines = vm_text.split('\n')
        commands = _Preprocessor().process(lines)
        asm_parts = map(self.get_asm, commands)
        return ''.join(asm_parts)

    def get_asm(self, command: str):
        cmd_type = self.command_part(command)
        if cmd_type in const.ARITHMETIC_CMD:
            return Arithmetic(command).assembly()
        elif cmd_type in const.MEMORY_ACCESS_CMD:
            return MemoryAccess(command, self.file).assembly()
        else:
            return ''  # TODO

    def command_part(self, command: str):
        return command.split()[0].lower()


class _Preprocessor:

    def process(self, lines):
        commands = filter(self.is_command, lines)
        return map(self.remove_inline_comment, commands)

    def is_command(self, line: str):
        comment_line = line.lstrip().startswith('//')
        empty_line = line.isspace() or line == ''
        return not (comment_line or empty_line)

    def remove_inline_comment(self, line: str):
        return sub(r'//.+', '', line)
