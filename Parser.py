from enum import Enum


class commandType(Enum):
    C_Arithmetic = 1
    C_Push = 2
    C_Pop = 3
    C_Label = 4
    C_GOTO = 5
    C_If = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class Parser:
    def __init__(self, InputFile):
        self.plausibleCommands = {'add': commandType.C_Arithmetic,
                                  'sub': commandType.C_Arithmetic,
                                  'sum': commandType.C_Arithmetic,
                                  'mult': commandType.C_Arithmetic,
                                  'gt': commandType.C_Arithmetic,
                                  'lt': commandType.C_Arithmetic,
                                  'eq': commandType.C_Arithmetic,
                                  'neg': commandType.C_Arithmetic,
                                  'and': commandType.C_Arithmetic,
                                  'or': commandType.C_Arithmetic,
                                  'not': commandType.C_Arithmetic,
                                  'push': commandType.C_Push,
                                  'pop': commandType.C_Pop,
                                  'if-goto': commandType.C_If,
                                  'goto': commandType.C_GOTO,
                                  'label': commandType.C_Label,
                                  'function': commandType.C_FUNCTION,
                                  'return': commandType.C_RETURN,
                                  'call': commandType.C_CALL}
        self.commandList = []
        self.currentCommandIndex = 0
        self.currentCommand = ' '
        self.splittedCommand = self.currentCommand.split()
        self.file = open(InputFile, 'r')
        for line in self.file:
            splittedLine = line.split()
            if splittedLine != [] and splittedLine[0] in self.plausibleCommands:
                self.commandList.append(line.rsplit('//', 1)[0].strip())
        self.currentCommand = self.commandList[0]

    def hasMoreCommands(self):
        return self.currentCommandIndex != len(self.commandList)

    def advance(self):
        self.currentCommandIndex += 1
        if self.hasMoreCommands():
            self.currentCommand = self.commandList[self.currentCommandIndex]
            return self.currentCommand

    def commandType(self):
        self.plausibleCommands = {'add': commandType.C_Arithmetic,
                                  'sub': commandType.C_Arithmetic,
                                  'sum': commandType.C_Arithmetic,
                                  'mult': commandType.C_Arithmetic,
                                  'push': commandType.C_Push,
                                  'pop': commandType.C_Pop,
                                  'if': commandType.C_If,
                                  'function': commandType.C_FUNCTION,
                                  'return': commandType.C_RETURN,
                                  'call': commandType.C_CALL}

    def arg1(self):
        if self.splittedCommand[0] in self.plausibleCommands:
            return self.plausibleCommands[self.splittedCommand[0]]

    def arg2(self):
        if self.splittedCommand[1] in self.plausibleCommands:
            return self.plausibleCommands[self.splittedCommand[0]]

    def checkParser(self):
        while self.hasMoreCommands():
            print(self.currentCommand)
            self.advance()

    def Close(self):
        self.file.close()

    def getCurrentCommand(self):
        return str(self.currentCommand)


# test = Parser(
#     '/home/Nand2TetrisCourse/nand2tetris/projects/07/MemoryAccess/BasicTest/BasicTest.vm')
# test.checkParser()
