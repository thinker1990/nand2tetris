from argparse import ArgumentParser
from pathlib import Path
from jack_compiler import Compiler


def source_path():
    ap = ArgumentParser()
    ap.add_argument('jack')
    args = ap.parse_args()
    return Path(args.jack)


def source_jacks(path):
    if not path.exists():
        raise(f'{path.name} does not exists.')
    if path.is_dir():
        return path.glob('*.jack')
    else:
        return [f for f in [path] if f.suffix == '.jack']


def parse(jack):
    vm = Compiler().parse(jack.read_text())
    target_vm(jack).write_text(vm)


def target_vm(source_path):
    directory = source_path.parent
    vm = f'{source_path.stem}.vm'
    return directory.joinpath(vm)


if __name__ == '__main__':
    path = source_path()
    for jack in source_jacks(path):
        parse(jack)
