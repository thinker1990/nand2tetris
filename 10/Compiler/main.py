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
    xml = Compiler().parse(jack.read_text())
    target_xml(jack).write_text(xml)


def target_xml(source_path):
    directory = source_path.parent
    xml = f'{source_path.stem}.xml'
    return directory.joinpath(xml)


if __name__ == '__main__':
    path = source_path()
    map(parse, source_jacks(path))
