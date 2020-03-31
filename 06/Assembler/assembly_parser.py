from re import sub
from enum import Enum


class AssemblyParser:

    def parse(self, assembly):
        pure_asm = _Preprocessor().process(assembly)
        return [*map(self.parse_line, pure_asm)]

    def parse_line(self, command):
        if command.startswith('@'):
            return A_Command(command)
        elif command.startswith('('):
            return L_Command(command)
        else:
            return C_Command(command)


class A_Command:

    def __init__(self, command):
        self.text = command

    def symbol(self):
        return self.text.lstrip('@')


class L_Command:

    def __init__(self, command):
        self.text = command

    def label(self):
        return self.text.strip('()')


class C_Command:

    _EMPTY = 'null'

    def __init__(self, command):
        self.text = command

    def dest(self):
        if self.text.find('=') > 0:
            return self.text.split('=')[0]
        else:
            return self._EMPTY

    def comp(self):
        part = self.text.split(';')[0]
        if part.find('=') > 0:
            return part.split('=')[1]
        else:
            return part

    def jump(self):
        if self.text.find(';') > 0:
            return self.text.split(';')[1]
        else:
            return self._EMPTY


class _Preprocessor:

    def process(self, assembly):
        commands = filter(self.is_command, assembly)
        commands_without_whitespace = map(self.remove_whitespace, commands)
        pure_commands = map(self.remove_inline_comment,
                            commands_without_whitespace)
        return pure_commands

    def is_command(self, line: str):
        comment_line = line.lstrip().startswith('//')
        empty_line = line.isspace()
        return not (comment_line or empty_line)

    def remove_whitespace(self, line: str):
        return sub(r'\s+', '', line)

    def remove_inline_comment(self, line: str):
        return sub(r'//.+', '', line)
