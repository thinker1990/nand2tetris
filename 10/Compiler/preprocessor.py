from re import sub


class Preprocessor:

    def process(self, text):
        txt = self.remove_comment(text)
        return self.remove_whitespace(txt)

    def remove_comment(self, text):
        txt = sub(r'//.*', '', text)
        return sub(r'/\*[\s\S]*?\*/', '', txt)

    def remove_whitespace(self, text):
        return sub(r'\s+', ' ', text)
