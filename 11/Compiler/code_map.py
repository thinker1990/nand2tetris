from uuid import uuid4


_ARG_TYPE_TO_SEG = {
    'static': 'static',
    'field': 'this',
    'argument': 'argument',
    'var': 'local'
}

_BIN_OP = {
    '+': 'add',
    '-': 'sub',
    '&': 'and',
    '|': 'or',
    '<': 'lt',
    '>': 'gt',
    '=': 'eq',
    '*': call_vm('Math.multiply', 2),
    '/': call_vm('Math.divide', 2)
}

_UNARY_OP = {
    '-': 'neg',
    '~': 'not'
}


def function_declaration_vm(name, nvar):
    return f'function {name} {nvar}'


def allocate_object_vm(obj_size):
    return merge(
        constant_vm(obj_size),
        call_vm('Memory.alloc', 1),
        pop_vm('pointer', 0)
    )


def adjust_this_vm():
    return merge(
        push_vm('argument', 0),
        pop_vm('pointer', 0)
    )


def let_statement_vm(target, value):
    return merge(
        value,
        target
    )


def if_statement_vm(condition, consequent, alternative):
    else_label = unique_label('ELSE')
    done_label = unique_label('IF_DONE')
    return merge(
        condition,
        'not',
        if_goto_vm(else_label),
        consequent,
        goto_vm(done_label),
        label_vm(else_label),
        alternative,
        label_vm(done_label)
    )


def while_statement_vm(test, loop_body):
    loop_label = unique_label('LOOP')
    done_label = unique_label('LOOP_DONE')
    return merge(
        label_vm(loop_label),
        test,
        'not',
        if_goto_vm(done_label),
        loop_body,
        goto_vm(loop_label),
        label_vm(done_label)
    )


def do_statement_vm(routine_call):
    return merge(
        routine_call,
        ignore_return_vm()
    )


def return_statement_vm(value):
    return merge(
        value,
        'return'
    )


def return_void_vm():
    return merge(
        constant_vm(0),
        'return'
    )


def assign_variable_vm(target):
    kind, offset = target
    return pop_vm(segment(kind), offset)


def assign_array_entry_vm(target, index):
    kind, offset = target
    return merge(
        push_vm(segment(kind), offset),
        index,
        'add',
        pop_vm('pointer', 1),
        pop_vm('that', 0)
    )


def inclass_call_vm(method, arguments):
    arg_list = list(arguments)
    narg = len(arg_list) + 1
    return merge(
        push_vm('pointer', 0),
        arg_list,
        call_vm(method, narg)
    )


def routine_call(method, arguments):
    arg_list = list(arguments)
    return merge(
        arg_list,
        call_vm(method, len(arg_list))
    )


def integer_vm(value):
    return constant_vm(value)


def string_vm(value):
    return merge(
        constant_vm(len(value)),
        call_vm('String.new', 1),
        map(append_char, value)
    )


def keyword_vm(word):
    if word in ('false', 'null'):
        return constant_vm(0)
    elif word == 'true':
        return merge(
            constant_vm(1),
            'neg'
        )
    else:
        return push_vm('pointer', 0)


def variable_vm(target):
    kind, offset = target
    return push_vm(segment(kind), offset)


def array_entry_vm(target, index):
    kind, offset = target
    return merge(
        push_vm(segment(kind), offset),
        index,
        'add',
        pop_vm('pointer', 1),
        push_vm('that', 0)
    )


def unary_vm(operator, term):
    return merge(
        term,
        unary_op_vm(operator)
    )


def append_char(char):
    return merge(
        constant_vm(ord(char)),
        call_vm('String.appendChar', 2)
    )


def segment(kind):
    return _ARG_TYPE_TO_SEG[kind]


def call_vm(method, narg):
    return f'call {method} {narg}'


def label_vm(symbol):
    return f'label {symbol}'


def goto_vm(label):
    return f'goto {label}'


def if_goto_vm(label):
    return f'if-goto {label}'


def unique_label(prefix='LABEL'):
    uid = uuid4().hex.upper()
    return f'{prefix}_{uid[:10]}'


def ignore_return_vm():
    return pop_vm('temp', 0)


def constant_vm(value):
    return push_vm('constant', value)


def push_vm(segment, index):
    return f'push {segment} {index}'


def pop_vm(segment, index):
    return f'pop {segment} {index}'


def binary_op_vm(operator):
    return _BIN_OP[operator]


def unary_op_vm(operator):
    return _UNARY_OP[operator]


def merge(*parts):
    flattened = flatten(parts)
    empty_trimmed = [item for item in flattened if item]
    return '\n'.join(empty_trimmed)


def flatten(nest_list):
    result = []
    for item in nest_list:
        if isinstance(item, str):
            result.append(item)
        else:
            result.extend(flatten(item))
    return result
