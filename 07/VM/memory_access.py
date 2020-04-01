
class MemoryAccess:

    def __init__(self, command):
        self.cmd, self.seg, self.idx = self.cmd_parts(command)

    def assembly(self):
        if self.seg == 'constant':
            return f'\n@{self.idx}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        else:
            return ''

    def cmd_parts(self, text):
        return tuple(text.lower().split())
