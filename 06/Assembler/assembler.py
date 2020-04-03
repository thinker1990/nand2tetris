from preprocessor import Preprocessor
from asm_parser import Parser
from symbol_table import SymbolTableBuilder
from code_generator import CodeGenerator


class Assembler():

    def assembly(self, asm):
        pure_asm = Preprocessor().process(asm)
        parsed_asm = Parser().parse(pure_asm)
        symbol_table = SymbolTableBuilder().build(parsed_asm)
        return CodeGenerator(symbol_table).generate(parsed_asm)
