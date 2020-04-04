from re import sub


class Preprocessor:

    def process(self, asm):
        no_comments = self.remove_comment(asm)
        return self.remove_whitespace(no_comments)

    def remove_comment(self, text):
        return sub(r'//.*', '', text)

    def remove_whitespace(self, text):
        return sub(r'[ \t]+', '', text)
