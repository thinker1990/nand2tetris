from preprocessor import Preprocessor
from tokenizer import Tokenizer
from analyzer import Analyzer
from xml_format import to_xml


class Compiler:

    def parse(self, jack):
        pure_jack = Preprocessor().process(jack)
        tokens = Tokenizer(pure_jack).tokens()
        parse_tree = Analyzer(tokens).parse_tree()
        return to_xml(parse_tree)
