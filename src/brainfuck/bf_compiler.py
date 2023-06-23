"""takes source code of brainfuck as input and convert it into LLVM IR"""
import os.path

from llvmlite import ir

from utils import strip_comments

Cell: ir.Type = ir.IntType(8)
LLVMInt: ir.Type = ir.IntType(32)
VoidFunc: ir.Type = ir.FunctionType(ir.VoidType(), [])


class Compiler:
    src: str

    module: ir.Module
    context: ir.Context

    def __init__(self, src: str):
        self.src = strip_comments(src)

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
        arr_ptr.initializer = Cell.as_pointer()(None)

        # c func
        c_getchar = ir.Function(module, ir.FunctionType(LLVMInt, []), name='getchar')
        c_putchar = ir.Function(module, ir.FunctionType(LLVMInt, [LLVMInt]), name='putchar')
        c_calloc = ir.Function(module, ir.FunctionType(Cell.as_pointer(), [LLVMInt, LLVMInt]), name='calloc')
        c_free = ir.Function(module, ir.FunctionType(ir.VoidType(), [Cell.as_pointer()]), name='free')

        # inc, dec, input, output, mov_left, mov_right
        llvm_inc = ir.Function(module, VoidFunc, name='inc')
        block = llvm_inc.append_basic_block(name='entry')
        with builder.goto_block(block):
            ptr = builder.gep(builder.load(arr_ptr), (builder.load(idx_ptr),))
            val = builder.add(builder.load(ptr), Cell(1))
            builder.store(val, ptr)
            builder.ret_void()

        llvm_dec = ir.Function(module, VoidFunc, name='dec')
        block = llvm_dec.append_basic_block(name='entry')
        with builder.goto_block(block):
            ptr = builder.gep(builder.load(arr_ptr), (builder.load(idx_ptr),))
            val = builder.sub(builder.load(ptr), Cell(1))
            builder.store(val, ptr)
            builder.ret_void()

        llvm_input = ir.Function(module, VoidFunc, name='input')
        block = llvm_input.append_basic_block(name='entry')
        with builder.goto_block(block):
            ptr = builder.gep(builder.load(arr_ptr), (builder.load(idx_ptr),))
            val = builder.trunc(builder.call(c_getchar, []), Cell)
            builder.store(val, ptr)
            builder.ret_void()

        llvm_output = ir.Function(module, VoidFunc, name='output')
        block = llvm_output.append_basic_block(name='entry')
        with builder.goto_block(block):
            ptr = builder.gep(builder.load(arr_ptr), (builder.load(idx_ptr),))
            val = builder.zext(builder.load(ptr), LLVMInt)
            builder.call(c_putchar, [val])
            builder.ret_void()

        llvm_mov_left = ir.Function(module, VoidFunc, name='mov_left')
        block = llvm_mov_left.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.sub(builder.load(idx_ptr), LLVMInt(1))
            builder.store(idx, idx_ptr)
            builder.ret_void()

        llvm_mov_right = ir.Function(module, VoidFunc, name='mov_right')
        block = llvm_mov_right.append_basic_block(name='entry')
        with builder.goto_block(block):
            idx = builder.add(builder.load(idx_ptr), LLVMInt(1))
            builder.store(idx, idx_ptr)
            builder.ret_void()

        # init array
        array_size = LLVMInt(2 ** 16)
        array = builder.call(c_calloc, [array_size, LLVMInt(1)])
        builder.store(array, arr_ptr)

        # build irs
        stack = []
        loop_count = 0
        for cmd in self.src:
            match cmd:
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
                    body = func.append_basic_block(name=f'body_{loop_count}')
                    end = func.append_basic_block(name=f'end_{loop_count}')
                    stack.append((body, end))
                    ptr = builder.gep(builder.load(arr_ptr), (builder.load(idx_ptr),))
                    cond = builder.icmp_unsigned('!=', builder.load(ptr), Cell(0))
                    loop_count += 1
                    builder.cbranch(cond, body, end)
                    builder.position_at_end(body)
                case ']':
                    body, end = stack.pop()
                    ptr = builder.gep(builder.load(arr_ptr), (builder.load(idx_ptr),))
                    cond = builder.icmp_unsigned('!=', builder.load(ptr), Cell(0))
                    builder.cbranch(cond, body, end)
                    builder.position_at_end(end)
                case _:
                    raise ValueError(f'unknown command: {cmd}')
        builder.call(c_free, [array])
        builder.ret_void()

        return module


def compile_bf(src: str) -> ir.Module:
    """compile the source code into a module and return its code"""
    compiler = Compiler(src)
    return compiler.compile()


def main(filename: str | None = None):
    if filename is None:
        src = input('Enter brainfuck source code below:\n')
        print(compile_bf(src))
    else:
        with open(filename, 'r', encoding='utf8') as f:
            src = f.read()
        with open(os.path.splitext(filename)[0]+'.ll', 'w', encoding='utf8') as f:
            f.write(str(compile_bf(src)))


if __name__ == '__main__':
    main('../../examples/add.bf')
