from command import A_Command, C_Command, L_Command


class Parser:

    def parse(self, asm):
        lines = asm.split('\n')
        return [*map(self.parse_line, lines)]

    def parse_line(self, text):
        if text.startswith('@'):
            return A_Command(text)
        elif text.startswith('('):
            return L_Command(text)
        else:
            return C_Command(text)
