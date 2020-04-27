from uuid import uuid4


def function_dec_vm(name, narg):
    return f'function {name} {narg}'


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


def return_void_vm():
    return merge(
        constant_vm(0),
        'return'
    )


def ignore_return_vm():
    return pop_vm('temp', 0)


def constant_vm(value):
    return push_vm('constant', value)


def true_vm():
    return merge(
        false_vm(),
        operator_vm('neg')
    )


def false_vm():
    return constant_vm(0)


def this_vm():
    return push_vm('pointer', 0)


def push_vm(segment, index):
    return f'push {segment} {index}'


def pop_vm(segment, index):
    return f'pop {segment} {index}'


def operator_vm(op):
    return op


def merge(self, *parts):
    flatten = [i for sub in parts for i in sub]
    return '\n'.join(flatten)
