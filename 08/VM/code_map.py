from re import sub
from uuid import uuid4


# Common assembly segments:
POP = '''@SP
         M=M-1
         @SP
         A=M'''

PUSH = '''@SP
          A=M
          M=D
          @SP
          M=M+1'''


# Arithmetic assembly segments:
UNARY = f'''{POP}
            D={{op}}M
            {PUSH}'''

BINARY = f'''{POP}
             D=M
             {POP}
             D=M{{op}}D
             {PUSH}'''

LOGICAL = f'''{POP}
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

ARITHMETIC_ASM = {
    'add': BINARY.format(op='+'),
    'sub': BINARY.format(op='-'),
    'neg': UNARY.format(op='-'),
    'and': BINARY.format(op='&'),
    'or': BINARY.format(op='|'),
    'not': UNARY.format(op='!'),
    'eq': LOGICAL.format(jump='JEQ'),
    'gt': LOGICAL.format(jump='JGT'),
    'lt': LOGICAL.format(jump='JLT')
}


def arithmetic_asm(vm_cmd):
    asm = ARITHMETIC_ASM[vm_cmd]
    if vm_cmd in ('eq', 'gt', 'lt'):
        asm = make_label_unique(asm)
    return asm


def make_label_unique(asm):
    return sub(r'UID', unique_id(), asm)


def unique_id():
    uid = uuid4().hex.upper()
    return uid[:10]


# Memory access assembly segments:
CONSTANT = '''@{idx}'''

RAM_REF = '''@{base}
             D=M
             @{idx}
             A=D+A'''

REGISTER = '''@{base}
              D=A
              @{idx}
              A=D+A'''

STATIC = '''@{file}.{idx}'''

SEGMENTS = {
    'constant': (CONSTANT, None),
    'local': (RAM_REF, 'LCL'),
    'argument': (RAM_REF, 'ARG'),
    'this': (RAM_REF, 'THIS'),
    'that': (RAM_REF, 'THAT'),
    'pointer': (REGISTER, 'THIS'),
    'temp': (REGISTER, 'R5'),
    'static': (STATIC, None)
}

PUSH_CONST = f'''{{SET_A}}
                 D=A
                 {PUSH}'''

PUSH_ASM = f'''{{SET_A}}
               D=M
               {PUSH}'''

POP_ASM = f'''{{SET_A}}
              D=A
              @R15
              M=D
              {POP}
              D=M
              @R15
              A=M
              M=D'''


def push_asm(segment, index, file):
    tpl, reg = SEGMENTS[segment]
    addr = tpl.format(base=reg, idx=index, file=file)
    if segment == 'constant':
        return PUSH_CONST.format(SET_A=addr)
    else:
        return PUSH_ASM.format(SET_A=addr)


def pop_asm(segment, index, file):
    tpl, reg = SEGMENTS[segment]
    addr = tpl.format(base=reg, idx=index, file=file)
    return POP_ASM.format(SET_A=addr)


# Program flow assembly segments:
def label_asm(label):
    return f'({label})'


def goto_asm(label):
    return f'''@{label}
               0;JMP'''


def if_goto_asm(label):
    return f'''{POP}
               D=M
               @{label}
               D;JNE'''
