from argparse import ArgumentParser
from pathlib import Path
from assembly_parser import AssemblyParser
from symbol_table import SymbolTableBuilder
from assembly_decoder import AssemblyDecoder


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('asm')
    args = ap.parse_args()
    asm_file = args.asm

    path = Path(asm_file)
    if not path.is_file():
        raise(f'file {asm_file} does not exists.')

    with open(asm_file, 'r') as source:
        assembly = source.readlines()

        parsed_asm = AssemblyParser().parse(assembly)
        symbol_table = SymbolTableBuilder().build(parsed_asm)
        binary = AssemblyDecoder(symbol_table).generate_binary_code(parsed_asm)

        with open(f'{path.stem}.hack', 'w') as target:
            target.writelines(binary)
