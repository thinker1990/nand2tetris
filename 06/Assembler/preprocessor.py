from re import sub


class Preprocessor:

    def process(self, asm):
        cmds = filter(self.command, asm.split('\n'))
        cmds = map(self.remove_inline_comment, cmds)
        cmds = map(self.remove_whitespace, cmds)
        return '\n'.join(cmds)

    def command(self, line):
        comment = line.lstrip().startswith('//')
        blank = line.isspace() or line == ''
        return not (comment or blank)

    def remove_inline_comment(self, line):
        return sub(r'//.*', '', line)

    def remove_whitespace(self, line):
        return sub(r'[ \t]+', '', line)
