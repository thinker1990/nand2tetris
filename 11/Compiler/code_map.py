from uuid import uuid4


_ARG_KIND_TO_SEG = {
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
    '*': 'call Math.multiply 2',
    '/': 'call Math.divide 2'
}

_UNARY_OP = {
    '-': 'neg',
    '~': 'not'
}


def method_name(routine_name, class_name):
    return f'{class_name}.{routine_name}'


def method_declaration_vm(name, nvar):
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


def call_inclass_vm(method, arguments):
    return merge(
        push_vm('pointer', 0),
        call_method_vm(method, arguments, len(arguments) + 1)
    )


def call_instance_vm(target, method, arguments):
    return merge(
        variable_vm(target),
        call_method_vm(method, arguments, len(arguments) + 1)
    )


def call_static_vm(method, arguments):
    return call_method_vm(method, arguments, len(arguments))


def call_method_vm(method, arguments, narg):
    return merge(
        arguments,
        call_vm(method, narg)
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
    else:  # this
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


def ignore_return_vm():
    return pop_vm('temp', 0)


def append_char(char):
    return merge(
        constant_vm(ord(char)),
        call_vm('String.appendChar', 2)
    )


def segment(kind):
    return _ARG_KIND_TO_SEG[kind]


def binary_op_vm(operator):
    return _BIN_OP[operator]


def unary_op_vm(operator):
    return _UNARY_OP[operator]


def call_vm(method, narg):
    return f'call {method} {narg}'


def label_vm(symbol):
    return f'label {symbol}'


def goto_vm(label):
    return f'goto {label}'


def if_goto_vm(label):
    return f'if-goto {label}'


def constant_vm(value):
    return push_vm('constant', value)


def push_vm(segment, index):
    return f'push {segment} {index}'


def pop_vm(segment, index):
    return f'pop {segment} {index}'


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


def unique_label(prefix='LABEL'):
    uid = uuid4().hex.upper()
    return f'{prefix}_{uid[:10]}'
