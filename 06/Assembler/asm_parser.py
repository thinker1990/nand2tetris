from command import A_Command, C_Command, L_Command


class Parser:

    def parse(self, asm):
        lines = asm.split()
        return [*map(self.parse_line, lines)]

    def parse_line(self, command):
        if command.startswith('@'):
            return A_Command(command)
        elif command.startswith('('):
            return L_Command(command)
        else:
            return C_Command(command)
