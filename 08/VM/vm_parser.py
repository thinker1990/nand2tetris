from command import *


class Parser():

    _ARITHMETIC_CMD = ('add', 'sub', 'neg', 'and',
                       'or', 'not', 'eq', 'gt', 'lt')
    _MEMORY_ACCESS_CMD = ('push', 'pop')
    _PROGRAM_FLOW_CMD = ('label', 'goto', 'if-goto')

    def parse(self, vm):
        lines = vm.split('\n')
        return [*map(self.parse_line, lines)]

    def parse_line(self, text):
        if self.cmd_of(text) in self._ARITHMETIC_CMD:
            return Arithmetic(text)
        elif self.cmd_of(text) in self._MEMORY_ACCESS_CMD:
            return MemoryAccess(text)
        elif self.cmd_of(text) in self._PROGRAM_FLOW_CMD:
            return ProgramFlow(text, 'main')  # TODO: func name
        else:
            raise(f'Command {text} not defined.')

    def cmd_of(self, text):
        return text.split()[0]
