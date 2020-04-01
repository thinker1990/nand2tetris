from re import sub
from uuid import uuid4


class Arithmetic:

    _POP = '''@SP
              M=M-1
              @SP
              A=M'''

    _PUSH = '''M=D
               @SP
               M=M+1'''

    _BINARY_OP = f'''
        {_POP}
        D=M
        {_POP}
        D=D{{op}}M
        {_PUSH}'''

    _UNARY_OP = f'''
        {_POP}
        D={{op}}D
        {_PUSH}'''

    _LOGICAL_OP = f'''
        {_POP}
        D=M
        {_POP}
        D=D-M
        @IF_TRUE_{{{{uid}}}}
        D;{{jump}}
        D=0
        {_PUSH}
        @CONTINUE_{{{{uid}}}}
        0;JMP
        (IF_TRUE_{{{{uid}}}})
        D=-1
        {_PUSH}
        (CONTINUE_{{{{uid}}}})'''

    _COMMAND_TO_ASSEMBLY = {
        'add': _BINARY_OP.format(op='+'),
        'sub': _BINARY_OP.format(op='-'),
        'neg': _UNARY_OP.format(op='-'),
        'and': _BINARY_OP.format(op='&'),
        'or': _BINARY_OP.format(op='|'),
        'not': _UNARY_OP.format(op='!'),
        'eq': _LOGICAL_OP.format(jump='JEQ'),
        'gt': _LOGICAL_OP.format(jump='JGT'),
        'lt': _LOGICAL_OP.format(jump='JLT')
    }

    _LOGICAL_CMD = ('eq', 'gt', 'lt')

    def __init__(self, command):
        self.command = command.strip().lower()

    def assembly(self):
        asm = self._COMMAND_TO_ASSEMBLY[self.command]
        if self.command in self._LOGICAL_CMD:
            asm = asm.format(uid=self.unique_id())
        return self.format(asm)

    def unique_id(self):
        return uuid4().hex

    def format(self, asm):
        return sub(r'[ \t]+', '', asm)
