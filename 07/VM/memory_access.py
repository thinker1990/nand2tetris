from re import sub
from constants import POP, PUSH


class MemoryAccess:

    _CONSTANT = '@{idx}'

    _RAM_REF = '''@{base}
                  D=M
                  @{idx}
                  A=D+A'''

    _REGISTER = '''@{base}
                   D=A
                   @{idx}
                   A=D+A'''

    _STATIC = '@{file}.{idx}'

    _ASM_TEMPLATE = {
        'constant': (_CONSTANT, None),
        'local': (_RAM_REF, 'LCL'),
        'argument': (_RAM_REF, 'ARG'),
        'this': (_RAM_REF, 'THIS'),
        'that': (_RAM_REF, 'THAT'),
        'pointer': (_REGISTER, 'THIS'),
        'temp': (_REGISTER, 'R5'),
        'static': (_STATIC, None)
    }

    _PUSH_ASM = f'''
        {{set_addr}}
        D=M
        {PUSH}'''

    _PUSH_CONST = f'''
        {{set_addr}}
        D=A
        {PUSH}'''

    _POP_ASM = f'''
        {{set_addr}}
        D=A
        @R15
        M=D
        {POP}
        D=M
        @R15
        A=M
        M=D'''

    def __init__(self, command, file_name):
        self.file = file_name
        self.cmd, self.seg, self.idx = self.cmd_parts(command)

    def cmd_parts(self, text):
        return tuple(text.lower().split())

    def assembly(self):
        if self.cmd == 'push':
            asm = self.push_asm()
        else:
            asm = self.pop_asm()
        return self.format(asm)

    def push_asm(self):
        tpl, reg = self._ASM_TEMPLATE[self.seg]
        addr = tpl.format(base=reg, idx=self.idx, file=self.file)
        if self.seg == 'constant':
            return self._PUSH_CONST.format(set_addr=addr)
        else:
            return self._PUSH_ASM.format(set_addr=addr)

    def pop_asm(self):
        tpl, reg = self._ASM_TEMPLATE[self.seg]
        addr = tpl.format(base=reg, idx=self.idx, file=self.file)
        return self._POP_ASM.format(set_addr=addr)

    def format(self, asm):
        return sub(r'[ \t]+', '', asm)
