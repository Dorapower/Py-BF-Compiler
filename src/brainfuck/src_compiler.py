"""takes source code of brainfuck as input and convert it into LLVM IR"""
from llvmlite import ir

from src_parser import parse

Cell: ir.Type = ir.IntType(8)
LLVMInt: ir.Type = ir.IntType(32)
VoidFunc: ir.Type = ir.FunctionType(ir.VoidType(), [])


class Compiler:
    src: str

    module: ir.Module
    context: ir.Context

    def __init__(self, src: str):
        self.src = src

        self.module = ir.Module(name="brainfuck")
        self.context = self.module.context

    def compile(self) -> ir.Module:
        """compile the ast into a module and return its code"""
        return self.build_function()

    def build_function(self) -> ir.Module:
        """
        read the ast and compile each command iteratively
        result is stored in a function named main, call it to run the logic
        """

        module = ir.Module(name='brainfuck')
        builder = ir.IRBuilder()

        # main func
        func = ir.Function(module, VoidFunc, name='main')
        block = func.append_basic_block(name='entry')
        builder.position_at_end(block)

        # idx, arr
        idx_ptr = ir.GlobalVariable(module, LLVMInt, name='index')
        idx_ptr.initializer = LLVMInt(0)
        arr_ptr = ir.GlobalVariable(module, Cell.as_pointer(), name='array')  # init in main

        # c func
        c_getchar = ir.Function(module, ir.FunctionType(LLVMInt, []), name='getchar')
        c_putchar = ir.Function(module, ir.FunctionType(LLVMInt, [LLVMInt]), name='putchar')
        c_calloc = ir.Function(module, ir.FunctionType(Cell.as_pointer(), [LLVMInt, LLVMInt]), name='calloc')
        c_free = ir.Function(module, ir.FunctionType(ir.VoidType(), [Cell.as_pointer()]), name='free')

        # inc, dec, input, output, mov_left, mov_right
        llvm_inc = ir.Function(module, VoidFunc, name='inc')
        block = llvm_inc.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.load(idx_ptr)
            arr = builder.load(arr_ptr)
            ptr = builder.gep(arr, (idx,))
            val = builder.load(ptr)
            val = builder.add(val, Cell(1))
            builder.store(val, ptr)

        llvm_dec = ir.Function(module, VoidFunc, name='dec')
        block = llvm_dec.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.load(idx_ptr)
            arr = builder.load(arr_ptr)
            ptr = builder.gep(arr, (idx,))
            val = builder.load(ptr)
            val = builder.sub(val, Cell(1))
            builder.store(val, ptr)
            builder.ret_void()

        llvm_input = ir.Function(module, VoidFunc, name='input')
        block = llvm_input.append_basic_block(name='entry')
        with builder.goto_block(block):
            val = builder.call(c_getchar, [])
            val = builder.trunc(val, Cell)
            idx = builder.load(idx_ptr)
            arr = builder.load(arr_ptr)
            ptr = builder.gep(arr, (idx,))
            builder.store(val, ptr)
            builder.ret_void()

        llvm_output = ir.Function(module, VoidFunc, name='output')
        block = llvm_output.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.load(idx_ptr)
            arr = builder.load(arr_ptr)
            ptr = builder.gep(arr, (idx,))
            val = builder.load(ptr)
            val = builder.zext(val, LLVMInt)
            builder.call(c_putchar, [val])
            builder.ret_void()

        llvm_mov_left = ir.Function(module, VoidFunc, name='mov_left')
        block = llvm_mov_left.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.load(idx_ptr)
            idx = builder.sub(idx, LLVMInt(1))
            builder.store(idx, idx_ptr)
            builder.ret_void()

        llvm_mov_right = ir.Function(module, VoidFunc, name='mov_right')
        block = llvm_mov_right.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.load(idx_ptr)
            idx = builder.add(idx, LLVMInt(1))
            builder.store(idx, idx_ptr)
            builder.ret_void()

        # init array
        array_size = LLVMInt(2 ** 16)
        array = builder.call(c_calloc, [array_size, LLVMInt(1)])
        builder.store(array, arr_ptr)

        # build irs
        ast = parse(self.src)
        for node in ast.children:
            match node.command:
                case '+':
                    builder.call(llvm_inc, [])
                case '-':
                    builder.call(llvm_dec, [])
                case ',':
                    builder.call(llvm_input, [])
                case '.':
                    builder.call(llvm_output, [])
                case '<':
                    builder.call(llvm_mov_left, [])
                case '>':
                    builder.call(llvm_mov_right, [])
                case '[':
                    pass
                case ']':
                    pass
                case _:
                    pass
        builder.call(c_free, [array])
        builder.ret_void()

        return module


def compile(src: str) -> ir.Module:
    """compile the source code into a module and return its code"""
    compiler = Compiler(src)
    return compiler.compile()


def main(filename: str | None = None):
    if filename is None:
        src = input('Enter brainfuck source code below:\n')
    else:
        with open(filename, 'r', encoding='utf8') as f:
            src = f.read()
    print(compile(src))


if __name__ == '__main__':
    main('../../examples/add.bf')
