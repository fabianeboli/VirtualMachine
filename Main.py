from Parser import Parser
from CodeWriter import CodeWriter
import os


class main:
    def __init__(self, inputFile):
        p = Parser(inputFile)
        cw = CodeWriter(os.getcwd()+'/'+inputFile.split('/')[-3]+'/'+inputFile.split('/')[-2]+'/'+inputFile.split('/')[-2] + '.asm')
        while p.hasMoreCommands():
            if p.currentCommandIndex is 0:
                cw.writeInit()
            if p.currentCommand is not None and len(p.currentCommand) > 0:
                currentCommand = p.getCurrentCommand()
                splittedCurrCommand = currentCommand.split()
                command = splittedCurrCommand[0]
                if len(splittedCurrCommand) == 3:
                    segment = splittedCurrCommand[1]
                    index = splittedCurrCommand[2]
                    cw.WriteThreePartCommands(command, segment, index)
                elif len(splittedCurrCommand) == 2:
                    segment = splittedCurrCommand[1]
                    cw.WriteTwoPartCommands(command, segment)
                elif len(splittedCurrCommand) == 1:
                    cw.WriteOnePartCommands(command)
            #print(command)
            p.advance()
        p.Close()
        cw.Close()


# BasicTest = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/MemoryAccess/BasicTest/BasicTest.vm')
# PointerTest = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/MemoryAccess/PointerTest/PointerTest.vm')
# StaticTest = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/MemoryAccess/StaticTest/StaticTest.vm')
# SimpleAdd = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
# StackTest = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/StackArithmetic/StackTest/StackTest.vm')
Fibonacci = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/FunctionCalls/FibonacciElement/Main.vm')
SimpleTest = main('/home/Nand2TetrisCourse/nand2tetris/projects/07/FunctionCalls/SimpleFunction/SimpleFunction.vm')


        