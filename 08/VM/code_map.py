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


def push_asm(segment, index, file=None):
    tpl, reg = SEGMENTS[segment]
    addr = tpl.format(base=reg, idx=index, file=file)
    if segment == 'constant':
        return PUSH_CONST.format(SET_A=addr)
    else:
        return PUSH_ASM.format(SET_A=addr)


def pop_asm(segment, index, file=None):
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


# Function calling assembly segments:
def function_asm(name, var_count=0):
    return f'''({name})
               {init_vars(var_count)}'''


def call_asm(func, arg_count=0):
    ret = return_address()
    return f'''{save_ret(ret)}
               {save_calling('LCL')}
               {save_calling('ARG')}
               {save_calling('THIS')}
               {save_calling('THAT')}
               {reset_ARG(arg_count)}
               {reset_LCL()}
               {goto_label(func)}
               ({ret})'''


def return_asm():
    return f'''{called_frame()}
               {restore('RET', 5)}
               {return_value()}
               {restore_SP()}
               {restore('THAT', 1)}
               {restore('THIS', 2)}
               {restore('ARG', 3)}
               {restore('LCL', 4)}
               {goto_addr('RET')}'''


def init_vars(count):
    asms = [push_asm('constant', 0) for k in range(count)]
    return '\n'.join(asms)


def return_address():
    return f'RET_{unique_id()}'


def save_ret(addr):
    return f'''@{addr}
               D=A
               {PUSH}'''


def save_calling(reg):
    return f'''@{reg}
               D=M
               {PUSH}'''


def reset_ARG(count):
    return f'''@SP
               D=M
               @{count+5}
               D=D-A
               {set_to('ARG')}'''


def reset_LCL():
    return f'''@SP
               D=M
               {set_to('LCL')}'''


def goto_label(func):
    return goto_asm(func)


def called_frame():
    return f'''@LCL
               D=M
               {set_to('frame')}'''


def restore(target, offset):
    return f'''@frame
               D=M
               @{offset}
               A=D-A
               D=M
               {set_to(target)}'''


def return_value():
    return f'''{POP}
               D=M
               @ARG
               A=M
               M=D'''


def restore_SP():
    return f'''@ARG
               D=M+1
               {set_to('SP')}'''


def goto_addr(label):
    return f'''@{label}
               A=M
               0;JMP'''


# Bootstrap code:
def bootstrap_code():
    return f'''@256
               D=A
               {set_to('SP')}
               {call_asm('Sys.init')}'''


def set_to(location):
    return f'''@{location}
               M=D'''
