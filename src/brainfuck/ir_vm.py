"""takes llvm ir as input and execute it"""

import platform
import ctypes
from ctypes import CFUNCTYPE, c_void_p

import llvmlite.binding as llvm


def link_external_functions(engine: llvm.ExecutionEngine, module: llvm.ModuleRef, fn_name: str, fn_ptr: int):
    """Add external function to the execution engine"""
    func = module.get_function(fn_name)
    engine.add_global_mapping(func, fn_ptr)


def execute(src: str):
    """execute the llvm ir code"""
    # initialize llvm
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()

    # load external c functions
    match platform.system():
        case 'Windows':
            libc = ctypes.CDLL('msvcrt.dll')
        case 'Linux':
            libc = ctypes.CDLL('libc.so.6')
        case 'Darwin':
            libc = ctypes.CDLL('libc.dylib')
        case _:
            raise RuntimeError(f'Unsupported platform: {platform.system()}')

    c_calloc = libc.calloc
    c_free = libc.free
    c_getchar = libc.getchar
    c_putchar = libc.putchar

    # parse ir
    module = llvm.parse_assembly(src)
    module.verify()

    # create execution engine
    with llvm.create_mcjit_compiler(module, target_machine) as llvm_execution_engine:
        # link external functions
        link_external_functions(llvm_execution_engine, module, 'calloc', c_calloc)
        link_external_functions(llvm_execution_engine, module, 'free', c_free)
        link_external_functions(llvm_execution_engine, module, 'getchar', c_getchar)
        link_external_functions(llvm_execution_engine, module, 'putchar', c_putchar)

        llvm_execution_engine.finalize_object()
        llvm_execution_engine.run_static_constructors()

        # execute main function
        main_ptr = llvm_execution_engine.get_function_address('main')
        c_main = CFUNCTYPE(c_void_p)(main_ptr)
        c_main()

        llvm_execution_engine.run_static_destructors()


def main(filename: str | None = None):
    if filename is None:
        src = input('Enter llvm ir below:\n')
    else:
        with open(filename, 'r', encoding='utf8') as f:
            src = f.read()
    execute(src)


if __name__ == '__main__':
    main('../../examples/add.ll')
