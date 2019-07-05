class CodeWriter:
    def __init__(self, outputFile):
        self.outFile = open(outputFile, 'w')
        self.fileName = self.setFileName(
            outputFile.split('/')[-1].split('.')[0])
        self.labelCounter = 0
        self.arthJumpFlag = 0

    def setFileName(self, fileName):
        print(f'VM file {fileName} is started')
        self.moduleName = fileName

    def WriteOnePartCommands(self, command):
        OnePartCommands = {'add': self.addArithmetic,
                           'sub': self.subArithmetic,
                           'neg': self.negArithmetic,
                           'eq': self.eqArithmetic,
                           'gt': self.gtArithmetic,
                           'lt': self.ltArithmetic,
                           'and': self.AndArithmetic,
                           'or': self.OrArithmetic,
                           'not': self.NotArithmetic,
                           'return': self.writeReturn}
       
        if command in OnePartCommands:
            print('One part', command)
            OnePartCommands[command]()

    def WriteTwoPartCommands(self, command, label):
        TwoPartCommands = {'label': self.writeLabel,
                           'goto': self.writeGoto,
                           'if-goto': self.writeIf}
      
        if command in TwoPartCommands:
            print('Two part', command, label)
            TwoPartCommands[command](label)

    def WriteThreePartCommands(self, command, segment, index):
        ThreePartCommands = {'push': self.pushCommand,
                             'pop': self.PopCommand,
                             'call': self.writeCall,
                             'function': self.writeFunction
                             }
        
        if command in ThreePartCommands:
            print('ThreePart', command, segment, index)
            ThreePartCommands[command](segment, index)

    def Close(self):
        self.outFile.write('(END) \n')
        self.outFile.write('@END \n')
        self.outFile.write('0;JMP \n')
        self.outFile.close()

    def addArithmetic(self):
        self.arithmeticTemplate1()
        self.outFile.write('M=M+D  //add \n')

    def subArithmetic(self):
        self.arithmeticTemplate1()
        self.outFile.write('M=M-D //sub \n')

    def negArithmetic(self):
        self.outFile.write('D=0\n@SP\nA=M-1\nM=D-M\n')

    def eqArithmetic(self):
        # label = f'JEQ_{self.moduleName}_{self.symbolCounter}'
        self.arithmeticTemplate2('JNE')
        self.arthJumpFlag += 1

    def gtArithmetic(self):
        self.arithmeticTemplate2('JLE')
        self.arthJumpFlag += 1

    def ltArithmetic(self):
        self.arithmeticTemplate2('JGE')
        self.arthJumpFlag += 1

    def AndArithmetic(self):
        self.outFile.arithmeticTemplate1()
        self.outFile.write('M=D&M //And \n')

    def OrArithmetic(self):
        self.outFile.write('@SP\nA=M-1\nM=!M\n')
        self.outFile.write('M=D|M //Or \n')

    def NotArithmetic(self):
        self.outFile.write('@SP\nA=M-1\nM=D-M\n')

    def pushCommand(self, segment, index):
        # segments = {'constant': self.writePush('constant', index),
        #             'local': self.writePush('LCL', index, False),
        #             'argument': self.writePush('ARG', index, False),
        #             'this': self.writePush('THIS', index, False),
        #             'that': self.writePush('THAT', index, False),
        #             'temp': self.writePush('R5', index, False),
        #             'pointer': self.pointerPush(index),
        #             'static': self.writePush('static', index)
        #             }
        # #print('segment', segment, index)
        # if segment in segments:
        #     print('selected segment:(', segment, segments[segment], ")")
        #     return segments[segment]
        if segment == 'constant':
            self.outFile.write(f'@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'local':
            self.writePush('LCL', index)
        elif segment == 'argument':
            self.writePush('ARG', index)
        elif segment == 'this':
            self.writePush('THIS', index)
        elif segment == 'THAT':
            self.writePush('THAT', index)
        elif segment == 'temp':
            self.writePush('R5', index + 5)
        elif segment == 'pointer':
            self.pointerPush(index)
        elif segment == 'static':
            self.outFile.write(
                f'@{self.fileName}{index}\nD=M\n@SP\nA=M\nM=D\nM=M+1\n')

    def pointerPush(self, index):
        if index == 0:
            self.writePush('THIS', index, True)
        elif index == 1:
            self.writePush('THAT', index, True)

    def PopCommand(self, segment, index):
        # segments = {'local': self.writePop('LCL', index, False),
        #             'argument': self.writePop('ARG', index, False),
        #             'this': self.writePop('THIS', index, False),
        #             'that': self.writePop('THAT', index, False),
        #             'temp': self.writePop('R5', index, False),
        #             'pointer': self.pointerPop(index),
        #             'static': f'@{self.fileName}{index}\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'
        #             }
        # if segment in segments:
        #     return segments[segment]
        if segment == 'local':
            self.writePop('LCL', index, False)
        elif segment == 'argument':
            self.writePop('ARG', index, False)
        elif segment == 'this':
            self.writePop('THIS', index, False)
        elif segment == 'that':
            self.writePop('THAT', index, False)
        elif segment == 'temp':
            self.writePop('R5', index + 5, False)
        elif segment == 'pointer' and index == 0:
            self.writePop('THIS', index, True)
        elif segment == 'pointer' and index == 1:
            self.writePop('THAT', index, True)
        elif segment == 'static':
            self.outFile.write(
               "@" + fileName + index + "\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")


    def pointerPop(self, index):
        if index == 0:
            self.writePop('THIS', index, True)
        elif index == 1:
            self.writePop('THAT', index, True)

    def writePush(self, segment, index, isDirect=False):
        if isDirect:
            noPointer = f''
        else:
            noPointer = f'@{index}\nA=D+A\nD=M\n'
        self.outFile.write(f'@{segment} //TEST{index}{segment}\n')
        self.outFile.write(f'D=M \n')
        self.outFile.write(f'{noPointer}')
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'A=M \n')
        self.outFile.write(f'M=D \n')
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'M=M+1 \n')

    def writePop(self, segment, index, isDirect):
        if segment == 'temp':
            index += 5
        if isDirect:
            noPointer = f'D=A\n'
        else:
            noPointer = f'D=M\n@{index}\nD=D+A\n'
        self.outFile.write(f'@{segment} \n')
        self.outFile.write(f'{noPointer}')
        self.outFile.write(f'@R13 \n')
        self.outFile.write(f'M=D \n')
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'AM=M-1 \n')
        self.outFile.write(f'D=M \n')
        self.outFile.write(f'@R13 \n')
        self.outFile.write(f'A=M \n')
        self.outFile.write(f'M=D \n')
      
    def writeInit(self):
        # bootstrap = f'BootStrap_{self.fileName}'
        # Bootstrap Code
        self.outFile.write('@256 \n')
        self.outFile.write('D=A \n')
        self.outFile.write('@SP \n')
        self.outFile.write('M=D \n')
        # Sys.init
        
        self.writeCall('Sys.init', 0)
        # self.outFile.write(f'({bootstrap}) \n')
        # self.outFile.write(f'@{bootstrap} \n')
        # self.outFile.write(f'0;JMP \n')

    def writeLabel(self, label):
        self.outFile.write(f'({label}) \n')

    def writeGoto(self, label):
        self.outFile.write(f'@{label} \n')
        self.outFile.write(f'0;JMP \n')

    def writeIf(self, label):
        self.arithmeticTemplate1()
        self.outFile.write(f'@{label} \n')
        self.outFile.write('D;JNE \n')

    def writeCall(self, functionName, numArgs):
        self.labelCounter += 1
        returnLabel = f'Return_Label{self.labelCounter}'
        self.outFile.write(f'@{returnLabel} \n')
        self.outFile.write(f'D=A \n')
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'A=M \n')
        self.outFile.write(f'M=D \n')
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'M=M+1 \n')
        self.writePush('LCL', 0, True)
        self.writePush('ARG', 0, True)
        self.writePush('THIS', 0, True)
        self.writePush('THAT', 0, True)
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'D=M \n')
        self.outFile.write(f'@5 \n')
        self.outFile.write(f'D=D-A \n')
        self.outFile.write(f'@{numArgs} \n')
        self.outFile.write(f'D=D-A \n')
        self.outFile.write(f'@ARG \n')
        self.outFile.write(f'M=D \n')
        self.outFile.write(f'@SP \n')
        self.outFile.write(f'D=M \n')
        self.outFile.write(f'@LCL \n')
        self.outFile.write(f'M=D \n')
        self.outFile.write(f'@{functionName} \n')
        self.outFile.write(f'0;JMP \n')
        self.outFile.write(f'({returnLabel}) \n')

    def writeReturn(self):
        # FRAME = LCL
        self.outFile.write('@LCL //RETURN \n')
        self.outFile.write('D=M \n')
        self.outFile.write('@R11 \n')
        self.outFile.write('M=D \n')
        # RET = *(FRAME - 5)
        self.outFile.write('@5 \n')
        self.outFile.write('A=D-A \n')
        self.outFile.write('D=M \n')
        self.outFile.write('@R12 \n')
        self.outFile.write('M=D \n')
        # *ARG = pop()
        self.writePop('ARG', 0, False)
        # SP = ARG + 1
        self.outFile.write('@ARG \n')
        self.outFile.write('D=M \n')
        self.outFile.write('@SP \n')
        self.outFile.write('M=D+1 \n')
        self.preTemplate('THAT')
        self.preTemplate('THIS')
        self.preTemplate('ARG')
        self.preTemplate('LCL')
        # goto RET
        self.outFile.write('@R12 \n')
        self.outFile.write('A=M \n')
        self.outFile.write('0;JMP //Koniec \n')

    def writeFunction(self, functionName, numLocals):
        self.outFile.write(f'({functionName}) \n')
        for i in range(int(numLocals)):
            self.pushCommand('constant', 0)

    def preTemplate(self, position):
        self.outFile.write('@R11 \n')
        self.outFile.write('D=M-1 \n')
        self.outFile.write('AM=D \n')
        self.outFile.write('D=M \n')
        self.outFile.write(f'@{position} \n')
        self.outFile.write('M=D \n')

    def arithmeticTemplate1(self):
        self.outFile.write(f'@SP\nAM=M-1\nD=M\nA=A-1\n')

    def arithmeticTemplate2(self, type):
        self.outFile.write(f'@SP\nAM=M-1\nD=M\nA=A-1\n')
        self.outFile.write(f'D=M-D\n@FALSE{self.arthJumpFlag}\n')
        self.outFile.write(f'D;{type}\n@SP\nA=M-1\nM=-1\n')
        self.outFile.write(f'@CONTINUE{self.arthJumpFlag}\n')
        self.outFile.write(f'0;JMP\n')
        self.outFile.write(f'(FALSE{self.arthJumpFlag})\n')
        self.outFile.write(f'@SP\nA=M-1\nM=0\n(CONTINUE{self.arthJumpFlag})\n')
