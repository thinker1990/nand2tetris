from argparse import ArgumentParser
from pathlib import Path
from vm import VM


def source_path():
    ap = ArgumentParser()
    ap.add_argument('vm')
    args = ap.parse_args()
    return Path(args.vm)


def source_vms(path):
    if not path.exists():
        raise(f'{path.name} does not exists.')
    if path.is_dir():
        return path.glob('*.vm')
    else:
        return [f for f in [path] if f.suffix == '.vm']


def target_assembly(source_path):
    directory = source_path.parent
    asm = f'{source_path.stem}.asm'
    return directory.joinpath(asm)


if __name__ == '__main__':
    path = source_path()
    vms = source_vms(path)
    assembly = VM().compile(vms)
    target_assembly(path).write_text(assembly)
