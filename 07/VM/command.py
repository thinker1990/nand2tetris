class Arithmetic:

    def __init__(self, command):
        self.text = command

    def operation(self):
        return self.text.strip()


class MemoryAccess:

    def __init__(self, command):
        self.op, self.seg, self.idx = tuple(command.split())

    def operation(self):
        return self.op

    def segment(self):
        return self.seg

    def index(self):
        return self.idx
