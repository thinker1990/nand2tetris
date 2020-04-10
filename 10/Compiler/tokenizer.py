from terminal import *


class Tokenizer:

    def __init__(self, jack):
        self.text = jack.strip()

    def tokens(self):
        while self.has_more():
            yield self.next_token()

    def has_more(self):
        return self.text != ''

    def next_token(self):
        word = self.next_word()
        if word in SYMBOLS:
            return (TOKEN_TYPE.SYMBOL, word)
        elif word in KEYWORDS:
            return (TOKEN_TYPE.KEYWORD, word)
        elif word.isnumeric():
            return (TOKEN_TYPE.INT_CONST, int(word))
        elif word.startswith('"') and word.endswith('"'):
            return (TOKEN_TYPE.STRING_CONST, word.strip('"'))
        else:
            return (TOKEN_TYPE.IDENTIFIER, word)

    def next_word(self):
        self.text = self.text.lstrip()
        word = self.text[0]
        if word in SYMBOLS:
            self.text = self.text[1:]
            return word
        # TODO
        