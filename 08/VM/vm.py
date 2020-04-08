from preprocessor import Preprocessor
from vm_parser import Parser
from code_generator import CodeGenerator


class VM:

    def compile(self, vms):
        bootstrap = CodeGenerator.bootstrap()
        asm_parts = map(self.compile_single, vms)
        return self.merge(bootstrap, asm_parts)

    def compile_single(self, vm):
        pure_vm = Preprocessor().process(vm.read_text())
        parsed_vm = Parser().parse(pure_vm)
        return CodeGenerator(vm.stem).generate(parsed_vm)

    def merge(self, bootstrap, parts):
        body = '\n'.join(parts)
        return '\n'.join([bootstrap, body])
