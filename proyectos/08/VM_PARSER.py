class VM_Parser:

    """Parser from VM to Hack Assembly Language"""

    def __init__(self,dir):

        """Open file if it exists or if it has permission."""

        try:
            self.file = open(dir)
        except (PermissionError, FileNotFoundError):
            print("ERROR: Can't open file, please check permissions or whether the file exists.")
            exit(1)  
        self.fileLines = self.file.readlines()
        self.fileLines = [x for x in self.fileLines if len(x.strip())!=0]  #Ignores empty lines
        self.currentCommand = None
        self.CommandType=None
        self.countLine = -1



    def hasMoreCommands(self):
        
        """Checks whether the file has more Commands or not."""

        if self.countLine < (len(self.fileLines)-1): return True
        return False



    def advance(self):

        """Reads line by line, until it finds a line with an Command"""

        while self.hasMoreCommands():
            self.countLine +=1
            self.currentCommand = self.fileLines[self.countLine]    
            self.currentCommand = self.ignoreCommentary()
            if len(self.currentCommand.strip()) != 0 : break
            if self.countLine == (len(self.fileLines)-1): break;
            


    def commandType(self):

        """Returns the command Type of the VM Command"""

        arithmetic_commands = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']

        if 'push' in self.currentCommand:
            self.CommandType= 'C_PUSH'
            return 'C_PUSH'
        elif 'pop' in self.currentCommand:
            self.CommandType= 'C_POP'
            return 'C_POP'
        elif 'label' in self.currentCommand.strip().split(' ')[0]:  # Label syntaxis label name_of_label
            self.CommandType= 'C_LABEL'
            return 'C_LABEL'
        elif 'if-goto' in self.currentCommand:
            self.CommandType= 'C_IF'
            return 'C_IF'
        elif 'return' in self.currentCommand:
            self.CommandType= 'C_RETURN'
            return 'C_RETURN'
        elif 'call' in self.currentCommand:
            self.CommandType= 'C_CALL'
            return 'C_CALL'
        elif self.currentCommand.strip() in arithmetic_commands:
            self.CommandType= 'C_ARITHMETIC'
            return 'C_ARITHMETIC'
        elif 'goto' in self.currentCommand:
            self.CommandType=  'C_GOTO' 
            return 'C_GOTO' 
        elif 'function' in self.currentCommand:
            self.CommandType= 'C_FUNCTION' 
            return 'C_FUNCTION'    
        

        print("ERROR: The command "+self.currentCommand.strip() +
                " does not belong to the virtual machine language")
        exit(1)



    def ignoreCommentary(self):

        """Ignores commentary of current Command, if it has one."""

        if "//" in self.currentCommand:
            arr = self.currentCommand.split("//")
            return arr[0]
        else:
            return self.currentCommand




    def arg1(self):

        """Returns the main instrucion of the VM Language """

        command_parts = self.currentCommand.strip().split(' ')

        # If it's only one word, it's beacuse it's an arithmetic Command or return/ but we only return the arithmetic Command
        if(len(command_parts)==1): return self.currentCommand       #Return all the Command
        
        return command_parts[1]              #Returns the main Command of the vm language
          


    def arg2(self):

        """Returns the second argument of the current command."""

        command_parts = self.currentCommand.strip().split(' ')
        arg3 = ['C_PUSH','C_POP','C_FUNCTION','C_CALL']                    #Commands' Type needed by arg2
        if(len(command_parts)==3 and self.CommandType in arg3):
            return command_parts[-1].strip()                               #Returns the last part
        
        print("ERROR: numbers of arguments is not meeted by "+self.currentCommand.strip() )
        exit(1)
