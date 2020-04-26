from parse_tree import *


class SymbolTable:

    def __init__(self, parsed: JackClass):
        self._variables = parsed.variables()
        self._routines = parsed.routines()

    def class_symbols(self):
        symbols = ClassSymbols()
        for dec in self._variables:
            for name in dec.names():
                symbols.define(name, dec.v_type(), dec.modifier())
        return symbols

    def method_symbols(self, name):
        routine = next(r for r in self._routines() if r.name() == name)
        symbols = MethodSymbols()
        for p in routine.parameters():
            symbols.define_argument(p.name(), p.param_type())
        for dec in routine.body().local_variables():
            for name in dec.names():
                symbols.define_local(name, dec.v_type())
        return symbols


class ClassSymbols:

    def __init__(self):
        self._table = {}
        self._static_idx = 0
        self._field_idx = 0

    def define(self, name, s_type, kind):
        if kind == 'static':
            index = self._static_idx
            self._static_idx += 1
        else:
            index = self._field_idx
            self._field_idx += 1
        self._table[name] = SymbolProperty(s_type, kind, index)

    def get(self, name):
        if name in self._table:
            return self._table[name]
        else:
            return None

    def count(self):
        return len(self._table)


class MethodSymbols:

    def __init__(self):
        self._table = {}
        self._arg_idx = 0
        self._var_idx = 0

    def define_argument(self, name, s_type):
        self._table[name] = SymbolProperty(s_type, 'argument', self._arg_idx)
        self._arg_idx += 1

    def define_local(self, name, s_type):
        self._table[name] = SymbolProperty(s_type, 'var', self._var_idx)
        self._var_idx += 1

    def get(self, name):
        if name in self._table:
            return self._table[name]
        else:
            return None


class SymbolProperty:

    def __init__(self, s_type, kind, index):
        self._type = s_type
        self._kind = kind
        self._index = index

    def s_type(self):
        return self._type

    def kind(self):
        return self._kind

    def index(self):
        return self._index
