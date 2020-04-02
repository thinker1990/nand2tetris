from re import sub
from uuid import uuid4
from constants import POP, PUSH


class Arithmetic:

    _UNARY = f'''
        {POP}
        D={{op}}M
        {PUSH}'''

    _BINARY = f'''
        {POP}
        D=M
        {POP}
        D=M{{op}}D
        {PUSH}'''

    _LOGICAL = f'''
        {POP}
        D=M
        {POP}
        D=M-D
        @IF_TRUE_UID
        D;{{jump}}
        D=0
        {PUSH}
        @CONTINUE_UID
        0;JMP
    (IF_TRUE_UID)
        D=-1
        {PUSH}
    (CONTINUE_UID)'''

    _COMMAND_TO_ASSEMBLY = {
        'add': _BINARY.format(op='+'),
        'sub': _BINARY.format(op='-'),
        'neg': _UNARY.format(op='-'),
        'and': _BINARY.format(op='&'),
        'or': _BINARY.format(op='|'),
        'not': _UNARY.format(op='!'),
        'eq': _LOGICAL.format(jump='JEQ'),
        'gt': _LOGICAL.format(jump='JGT'),
        'lt': _LOGICAL.format(jump='JLT')
    }

    def __init__(self, command):
        self.command = command.strip().lower()

    def assembly(self):
        asm = self._COMMAND_TO_ASSEMBLY[self.command]
        asm = self.make_label_unique(asm)
        return self.format(asm)

    def make_label_unique(self, asm):
        return sub(r'UID', self.unique_id(), asm)

    def unique_id(self):
        uuid = uuid4().hex.upper()
        return uuid[:10]

    def format(self, asm):
        return sub(r'[ \t]+', '', asm)
