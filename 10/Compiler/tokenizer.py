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
        first = self.first_letter()
        if first in SYMBOLS:
            return self.trimmed_symbol()
        elif first == '"':
            return self.trimmed_string()
        else:
            return self.trimmed_word()

    def first_letter(self):
        self.text = self.text.lstrip()
        return self.text[0]

    def trimmed_symbol(self):
        return self.trim_return(1)

    def trimmed_string(self):
        close_quote = self.text.find('"', 1)
        return self.trim_return(close_quote+1)

    def trimmed_word(self):
        idx = self.next_terminal_idx()
        return self.trim_return(idx)

    def next_terminal_idx(self):
        idx = 0
        while not (self.text[idx] in SYMBOLS or self.text[idx] == ' '):
            idx += 1
        return idx

    def trim_return(self, count):
        letters = self.text[:count]
        self.text = self.text[count:]
        return letters
