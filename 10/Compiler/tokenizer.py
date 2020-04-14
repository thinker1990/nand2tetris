from terminal import SYMBOLS
from token_store import TokenStore


class Tokenizer:

    def __init__(self, jack):
        self.text = jack.strip()
        self.store = TokenStore()

    def tokens(self):
        while self.has_more():
            self.store.push(self.next_word())
        return self.store

    def has_more(self):
        return self.text != ''

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
        return self.trim_and_return(1)

    def trimmed_string(self):
        close_quote = self.text.find('"', 1)
        return self.trim_and_return(close_quote+1)

    def trimmed_word(self):
        idx = self.next_terminal_idx()
        return self.trim_and_return(idx)

    def next_terminal_idx(self):
        idx = 0
        while not (self.text[idx] in SYMBOLS
                   or self.text[idx].isspace()):
            idx += 1
        return idx

    def trim_and_return(self, count):
        letters = self.text[:count]
        self.text = self.text[count:]
        return letters
