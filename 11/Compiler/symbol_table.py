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

    def define(self, name, s_type, kind):
        if kind == 'parameter':
            index = self._param_idx
            self._param_idx += 1
        else:
            index = self._local_idx
            self._local_idx += 1
        self._table[name] = SymbolProperty(s_type, kind, index)

    def get(self, name):
        if name in self._table:
            return self._table[name]
        else:
            return None

    def count(self):
        return len(self._table)


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
