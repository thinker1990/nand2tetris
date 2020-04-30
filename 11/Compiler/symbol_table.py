from parse_tree import *


class SymbolTable:

    def __init__(self):
        self._class_scope = {}
        self._method_scope = {}

    def add_class_symbols(self, parsed: JackClass):
        self._static_idx = 0
        self._field_idx = 0
        for var_dec in parsed.variables():
            self.define_class_var(var_dec)

    def add_method_symbols(self, routine: Subroutine):
        self._var_idx = 0
        if routine.modifier() == 'method':
            self._arg_idx = 1  # due to implicit first argument.
        else:
            self._arg_idx = 0
        for arg in routine.parameters():
            self.define_arg(arg)
        for dec in routine.body().local_variables():
            self.define_var(dec)

    def class_instance_size(self):
        return self._field_idx

    def method_var_count(self):
        return self._var_idx

    def defined(self, name):
        return (name in self._method_scope or
                name in self._class_scope)

    def where_is(self, var):
        _, kind, index = self.property_of(var)
        return kind, index

    def type_of(self, var):
        vtype, _, _ = self.property_of(var)
        return vtype

    def property_of(self, var):
        if not self.defined(var):
            raise Exception(f'{var} not defined.')
        if var in self._method_scope:
            vtype, kind, index = self._method_scope[var]
        else:
            vtype, kind, index = self._class_scope[var]
        return vtype, kind, index

    def define_class_var(self, dec: VariableDec):
        if dec.modifier() == 'static':
            index = self._static_idx
            self._static_idx += 1
        else:  # field
            index = self._field_idx
            self._field_idx += 1
        _property = (dec.var_type(), dec.modifier(), index)
        self._class_scope[dec.name()] = _property

    def define_arg(self, arg: Parameter):
        _property = (arg.param_type(), 'argument', self._arg_idx)
        self._method_scope[arg.name()] = _property
        self._arg_idx += 1

    def define_var(self, dec: VariableDec):
        _property = (dec.var_type(), 'var', self._var_idx)
        self._method_scope[dec.name()] = _property
        self._var_idx += 1
