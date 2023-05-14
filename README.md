# Py-BF-Compiler

A Brainfuck compiler implemented with Python

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

- [x] Lexer: convert src code into tokens (not required)
- [x] Parser: convert token/character string into an AST
- [ ] Interpreter: interpret the source code
- [ ] AST Interpreter: interpret the AST
- [ ] IRGen: generate IR from the AST
- [ ] IR Interpreter: interpret the IR

## Usage

To test the parser, run the `src_parser.py`