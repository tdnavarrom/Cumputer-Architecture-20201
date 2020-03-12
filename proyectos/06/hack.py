from code import Code
from symbolTable import SymbolTable
from parser import Parser
import sys

""" This first group of code is to add environmental variables to the code,
    they tell the compiler to read the file that is given as an enviromental variable
    and check if it's a '.asm' file, if it isn't, it returns an error, as it isn't a supported
    file of the Hack Assembly Language. """

args = sys.argv

if len(args) < 2:
    print("ERROR: please indicate the file to read.")
    exit(1)

file_name = args[1]
if not ".asm" in file_name:
    print("ERROR: file type not supported, must be '.asm'.")
    exit(1)

#Takes the name of the '.asm' file and adds it to the output file '.hack'

file_out = file_name.split('.asm')
file_out = file_out[0] + '.hack'

""" After reading the file, we start reading its content twice by
    calling the parser, and in the first run, we check any LOOP Tags
    inside the Assembly Code, add their line_of_code and their name in the Symbols Table,
    and add a 1 to the ROM counter, so the next LOOP tag, if there are more, may be added to the Symbols Table.
    The loop runs until there aren't instructions left to check inside the file.
"""

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

""" Then, we run the parser for the second twice, Where we now, start the translating each instruction
    of the code. We first check the instruction type, and then we start to 'extract' its content and
    translate it one by one, create a new line uniting them (because they compose one instruction after all) with and '/n' (new line)
    , and finally we add it to a String, that has all the translated code inside it.
    We finally add the Translated String into the output '.hack' file.
"""

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
