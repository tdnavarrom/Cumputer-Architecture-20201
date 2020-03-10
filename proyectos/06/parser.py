class Parser:

    """Parser for the Hack Assembly Language"""

    def __init__(self, dir):

        """Open file if it exists or if it has permission."""

        try:
            self.f=open(dir)
        except (PermissionError,FileNotFoundError) as e:
            print("ERROR: Can't open file, please check permissions or whether the file exists.")
            exit(1)
        self.fileLines = self.f.readlines()
        self.currentInstruction = None
        self.countLine=-1


    def hasMoreInstructions(self):

        """Checks whether the file has more instructions or not."""

        if self.countLine < (len(self.fileLines)-1): return True
        return False


    def nextLine(self):

        """ Reads line by line, until it finds a line with an instruction"""

        while True:
            self.countLine+=1
            self.currentInstruction = self.fileLines[self.countLine]
            self.currentInstruction = self.ignoreCommentary()
            if len(self.currentInstruction.strip()) != 0: break;
            if self.countLine == (len(self.fileLines)-1): break;


    def instructionType(self):

        """Checks the type of instruction."""

        if '@' in self.currentInstruction: return 'A_Instruction'
        elif '=' in self.currentInstruction or ';' in self.currentInstruction: return 'C_Instruction'
        elif '(' in self.currentInstruction and ')' in self.currentInstruction: return 'L_Instruction'
        elif '' in self.currentInstruction and self.countLine == (len(self.fileLines)-1): return 0
        else:
            print("ERROR: The instruction "+self.currentInstruction.strip()+" doesn't exists in the Hack Assembly Grammar")
            exit(1)


    def getSymbol(self):

        """Returns the symbol or decimal Xxx of the current command @Xxx or
           (Xxx). A_Instruction or L_Instruction"""

        currentLine = self.currentInstruction.strip()
        xxx = ""
        position = 1

        if len(currentLine) < 2:
            #Returns an error if just @ is in the instruction
            line_number = str(self.countLine)
            print("ERROR: Not enough parameters in A-Type-Instruction", line_number)
            exit(1)

        current_char = currentLine[position]

        if currentLine[0]=="(": instructionL = True #instructionL is true if instruction starts with '('

        #Reads current char to find all XXX values and returns them
        while current_char !=")" and current_char !="\n":
            xxx += current_char
            position += 1
            if position >= len(currentLine): break
            else: current_char = currentLine[position]

        currentLine=currentLine.strip()
        xxx=xxx.strip()

        if len(xxx)==0 and instructionL:
            #Exits with error if TAG instruction is incomplete
            line_number=str(self.countLine)
            print("ERROR: Missing arguments for the TAG Instruction in line: ", line_number)
            exit(1)

        if not xxx[0].isidentifier() and not xxx.isnumeric():
            #Returns error if the instruction isn't a number or a valid variable
            print("ERROR: Simbolo en el comando "+self.currentInstruction.strip()+" no es un identifiador")
            exit(1)

        return xxx.strip()


    def getDest(self):

        """Returns the dest mnemonic in the current
           C-Instruction (8 possi-bilities). C_INSTRUCTION"""

        if '=' in self.currentInstruction:   return self.currentInstruction.split('=')[0]
        else:   return ''


    def getComp(self):

        """Returns the comp mnemonic in the current C-Instruction"""

        currentLine =self.currentInstruction
        arr=""

        if "=" in currentLine:
            arr=currentLine.split("=")
            if ";" in arr[1]:
                arr1 = arr[1].split(";")
                mnemonic = arr1[0].strip()
                return mnemonic
            else:
                res = arr[1].split(" ")
                mnemonic = res[0].strip()
                return mnemonic
        if ";" in currentLine:
            arr = currentLine.split(";")
            return arr[0].strip()


    def jump(self):

        """Returns the jump mnemonic in the current C-command"""

        if ";" in self.currentInstruction:
            mnemonic = self.currentInstruction.split(';')[-1]
            return mnemonic[0:3]
        else:
            return ''


    def ignoreCommentary(self):

        """ignores commentary of current instruction, if it has one."""

        if "//" in self.currentInstruction:
            arr = self.currentInstruction.split("//")
            return arr[0]
        else:
            return self.currentInstruction
