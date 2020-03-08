from code import Code
from symbolTable import SymbolTable
from parser import Parser
import sys


args = sys.argv

if len(args) < 2:
    print("ERROR: please indicate the file to read.")
    exit(1)

file_name = args[1]
if not ".asm" in file_name:
    print("ERROR: file type not supported, must be '.asm'.")
    exit(1)

file_out = file_name.split('.asm')
file_out = file_out[0] + '.hack'

countROM=0
countRAM=16
final_instruction=''

firstRun = Parser(file_name)
symbolTable = SymbolTable()

while firstRun.hasMoreInstructions():
    firstRun.nextLine()
    type = firstRun.instructionType()
    if type == "L_Instruction":
        symbol = firstRun.getSymbol()

        if not symbolTable.contains(symbol):
            symbolTable.addEntry(symbol, countROM)

    else:
        countROM+=1

secondRun = Parser(file_name)

while secondRun.hasMoreInstructions():
    secondRun.nextLine()
    type = secondRun.instructionType()

    if type == "C_Instruction":

        instruction = "111"

        try:
            comp = secondRun.getComp()
            dest = secondRun.getDest()
            jump = secondRun.jump()

            instruction = instruction + Code.comp(comp) + Code.dest(dest) + Code.jump(jump)

        except KeyError:
            print("ERROR: Not valid arguments in ", secondRun.currentInstruction)
            exit(1)

        final_instruction = final_instruction + instruction + '\n'

    elif type == "A_Instruction":

        token = secondRun.getSymbol()

        if token.isnumeric():

            num = int(token)
            binary = format(num,"016b")
            final_instruction = final_instruction + binary + '\n'

        else:

            if symbolTable.contains(token):
                token = symbolTable.getAddress(token)
                num = int(token)
                binary = format(num, "016b")
                final_instruction = final_instruction + binary + "\n"

            elif token != "":
                symbolTable.addEntry(token, countRAM)
                countRAM += 1
                token = symbolTable.getAddress(token)
                num = int(token)
                binary = format(num, "016b")
                final_instruction = final_instruction + binary + "\n"

            else:
                print("ERROR: parameters not given for A-Type-Instriction in ", secondRun.currentInstruction)
                exit(1)


out = open(file_out,'w')
out.write(final_instruction)
