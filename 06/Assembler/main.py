from argparse import ArgumentParser
from pathlib import Path
from assembler import Assembler


def source_assembly():
    ap = ArgumentParser()
    ap.add_argument('asm')
    args = ap.parse_args()

    path = Path(args.asm)
    if path.is_file() and path.suffix == '.asm':
        return path
    else:
        raise('Assembly file required.')


def target_binary(source_path):
    directory = source_path.parent
    hack = f'{source_path.stem}.hack'
    return directory.joinpath(hack)


if __name__ == '__main__':
    asm = source_assembly()
    binary = Assembler().assembly(asm.read_text())
    target_binary(asm).write_text(binary)
