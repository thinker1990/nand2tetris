

class Arithmetic:

    _COMMAND_HANDLER = {
        'add': Arithmetic.add_asm,
        'sub': Arithmetic.sub_asm,
        'neg': Arithmetic.neg_asm,
        'and': Arithmetic.and_asm,
        'or': Arithmetic.or_asm,
        'not': Arithmetic.not_asm,
        'eq': Arithmetic.eq_asm,
        'gt': Arithmetic.gt_asm,
        'lt': Arithmetic.lt_asm
    }

    _POP_ONE_OPERAND = f'''
        @SP
        A=A-1
        D=M
    '''

    _POP_TWO_OPERANDS = f'''
        {Arithmetic._POP_ONE_OPERAND}
        @SP
        A=A-1
    '''

    _PUSH_RESULT = f'''
        M=D
        A=A+1
    '''

    def __init__(self, command):
        self.command = command.strip()

    def assembly(self):
        handler = self._COMMAND_HANDLER[self.command]
        return handler()

    def add_asm(self):
        return f'''
            {self._POP_TWO_OPERANDS}
            D=D+M
            {self._PUSH_RESULT}
        '''

    def sub_asm(self):
        return f'''
            {self._POP_TWO_OPERANDS}
            D=D-M
            {self._PUSH_RESULT}
        '''

    def neg_asm(self):
        return f'''
            {self._POP_ONE_OPERAND}
            D=-D
            {self._PUSH_RESULT}
        '''

    def and_asm(self):
        return f'''
            {self._POP_TWO_OPERANDS}
            D=D&M
            {self._PUSH_RESULT}
        '''

    def or_asm(self):
        return f'''
            {self._POP_TWO_OPERANDS}
            D=D|M
            {self._PUSH_RESULT}
        '''

    def not_asm(self):
        return f'''
            {self._POP_ONE_OPERAND}
            D=!D
            {self._PUSH_RESULT}
        '''
