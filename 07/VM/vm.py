from re import sub


class VM:

    def translate(self, vm_text):
        lines = vm_text.split('\n')
        commands = _Preprocessor().process(lines)
        parsed = map(self.parse, commands)

    def parse(self, command: str):
        cmd_type = self.command_part(command)
        parse_method = self._COMMAND_PARSE_MAP[cmd_type]
        return parse_method(command)

    def command_part(self, command: str):
        return command.split()[0].lower()

    def parse_add(self, command: str):
        return AddCommand(command)


class AddCommand:

    def assembly(self):
        pass


class _Preprocessor:

    def process(self, lines):
        commands = filter(self.is_command, lines)
        return map(self.remove_inline_comment, commands)

    def is_command(self, line: str):
        comment_line = line.lstrip().startswith('//')
        empty_line = line.isspace()
        return not (comment_line or empty_line)

    def remove_inline_comment(self, line: str):
        return sub(r'//.+', '', line)
