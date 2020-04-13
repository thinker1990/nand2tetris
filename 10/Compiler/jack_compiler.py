from preprocessor import Preprocessor
from tokenizer import Tokenizer
from analyzer import Analyzer
from terminal import TOKEN_TYPE


class Compiler:

    def parse(self, jack):
        pure_jack = Preprocessor().process(jack)
        tokens = Tokenizer(pure_jack).tokens()
        parse_tree = Analyzer().parse(tokens)
        return to_xml(parse_tree)


def to_xml(tree):
    tags = map(tag, tree)
    body = '\n'.join(tags)
    return f'<tokens>\n{body}\n</tokens>\n'


def tag(item):
    t, s = item
    if t == TOKEN_TYPE.SYMBOL:
        return f'<symbol> {trans(s)} </symbol>'
    elif t == TOKEN_TYPE.KEYWORD:
        return f'<keyword> {s} </keyword>'
    elif t == TOKEN_TYPE.INT_CONST:
        return f'<integerConstant> {s} </integerConstant>'
    elif t == TOKEN_TYPE.STRING_CONST:
        return f'<stringConstant> {s} </stringConstant>'
    else:
        return f'<identifier> {s} </identifier>'


def trans(s):
    if s == '<':
        return '&lt;'
    elif s == '>':
        return '&gt;'
    elif s == '"':
        return '&quot;'
    elif s == '&':
        return '&amp;'
    else:
        return s
