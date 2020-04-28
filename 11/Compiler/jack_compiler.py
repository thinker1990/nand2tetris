from preprocessor import Preprocessor
from tokenizer import Tokenizer
from analyzer import Analyzer
from symbol_table import SymbolTable
from code_generator import CodeGenerator


class Compiler:

    def parse(self, jack):
        pure_jack = Preprocessor().process(jack)
        tokens = Tokenizer(pure_jack).tokens()
        parse_tree = Analyzer(tokens).parse_tree()
        symbols = SymbolTable(parse_tree)
        return CodeGenerator(parse_tree, symbols).vm()
