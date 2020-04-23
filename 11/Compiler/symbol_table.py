from parse_tree import *


class SymbolTable:

    def __init__(self, parsed: JackClass):
        self._parsed = parsed

    def class_symbols(self):
        symbols = ClassSymbols()
        for dec in self._parsed.variables():
            for name in dec.names():
                symbols.define(name, dec.v_type(), dec.modifier())
        return symbols

    def method_symbols(self):
        mapping = {}
        for routine in self._parsed.routines():
            mapping[routine.name()] = self.method_symbol(routine)
        return mapping

    def method_symbol(self, routine):
        symbols = MethodSymbols()
        for p in routine.parameters():
            symbols.define_parameter(p.name(), p.param_type())
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
        self._param_idx = 0
        self._local_idx = 0

    def define_parameter(self, name, s_type):
        index = self._param_idx
        self._param_idx += 1
        self._table[name] = SymbolProperty(s_type, 'parameter', index)

    def define_local(self, name, s_type):
        index = self._local_idx
        self._local_idx += 1
        self._table[name] = SymbolProperty(s_type, 'var', index)

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
