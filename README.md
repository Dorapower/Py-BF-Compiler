# Py-BF-Runtime

A Brainfuck runtime implemented with Python. Consist of a static compiler,
a just-in-time compiler (both of them compile into LLVM IR) and an interpreter

## Grammar

The language is composed of eight commands, each of which is a character:

| Character | Meaning                                          |
|:---------:|:-------------------------------------------------|
|    `>`    | Increase the data ptr by one                     |
|    `<`    | Decrease the data ptr by one                     |
|    `+`    | Increment the byte at the ptr by one             |
|    `-`    | Decrement the byte at the prt by one             |
|    `.`    | Output the byte at the ptr                       |
|    `,`    | Accept one byte of input and store at the ptr    |
|    `[`    | Jump to the matching `]` if the data is zero     |
|    `]`    | Jump to the matching `[` if the data is non-zero |        

## Feature

- [x] Lexer: remove comment characters
- [x] Parser: convert commands string into an AST
- [x] Static compiler: convert AST into LLVM IR
- [x] VM: takes IR and execute it
- [ ] JIT compiler: convert part of AST into LLVM IR and execute it
- [x] Interpreter: directly execute on the source code

## Usage

1. download the src code
2. create a virtual environment (or not)
3. install the package: `pip install .`, dependencies will be installed automatically
4. test the modules by run them directly, or import them and call main function. 
Deal with the relative path carefully if you wish to input from files
