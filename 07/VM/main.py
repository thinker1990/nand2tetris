from argparse import ArgumentParser
from pathlib import Path
from vm import VM


def files_of(path):
    if not path.exists():
        raise(f'{path.name()} does not exists.')
    if path.is_dir():
        return path.iterdir()
    else:
        return [path]


def vm_file(path):
    return path.is_file() and path.suffix == '.vm'


def translate(vm):
    return VM(vm.stem).translate(vm.read_text())


def merge_assembly(parts):
    return ''.join(parts)


def target_assembly(path):
    return path.parent.joinpath(f'{path.stem}.asm')


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('vm_path')
    args = ap.parse_args()
    vm_path = args.vm_path

    path = Path(vm_path)
    vm_files = filter(vm_file, files_of(path))
    assembly_parts = map(translate, vm_files)
    assembly = merge_assembly(assembly_parts)
    target_assembly(path).write_text(assembly)
