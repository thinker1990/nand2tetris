class A_Command:

    def __init__(self, command):
        self.text = command

    def symbol(self):
        return self.text.lstrip('@')


class L_Command:

    def __init__(self, command):
        self.text = command

    def label(self):
        return self.text.strip('()')


class C_Command:

    _EMPTY = 'null'

    def __init__(self, command):
        self.text = command

    def dest(self):
        if self.text.find('=') > 0:
            return self.text.split('=')[0]
        else:
            return self._EMPTY

    def comp(self):
        part = self.text.split(';')[0]
        if part.find('=') > 0:
            return part.split('=')[1]
        else:
            return part

    def jump(self):
        if self.text.find(';') > 0:
            return self.text.split(';')[1]
        else:
            return self._EMPTY
