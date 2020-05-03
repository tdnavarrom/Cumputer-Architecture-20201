class VM_Writer:


    def __init__(self, output_filename):

        """ Writer for the translation between VM Language to Hack ASSEMBLY LANGUAGE"""

        output_filename = output_filename + '.asm'

        try:
            self.file = open(output_filename, 'w')
        except FileNotFoundError:
            print('Error: Could not create hack file')
            exit(1)
            self.file.close()

        self.hack_code = ''
        self.bool_count = 0
        self.call_count=0 
        self.currentFunction='';


    def set_output_filename(self, output_filename): 

        """Change output file name"""

        self.output_filename=output_filename


    def start_vm_file(self): 
        self.hack_code+=('move $t0,$sp\n')   #LOCAL
        self.hack_code+=('subiu $sp,$sp,4\n')
        self.hack_code+=('move $t1,$sp\n')   #ARGUMENT
        self.hack_code+=('subiu $sp,$sp,4\n')
        self.hack_code+=('move $t2,$sp\n')   #THIS
        self.hack_code+=('subiu $sp,$sp,4\n')
        self.hack_code+=('move $t3,$sp\n')   #THAT
        self.hack_code+=('subiu $sp,$sp,4\n\n')
        self.hack_code+=('move $t4,$sp\n')   #TEMP
        self.hack_code+=('subiu $sp,$sp,32\n')
        self.hack_code+=('move $t5,$sp\n')   #STATIC
        self.hack_code+=('subiu $sp,$sp,952\n\n')
        self.hack_code+=('move $t6,$sp\n')   #POINTER
        self.hack_code+=('subiu $sp,$sp,12\n\n')
        self.file.write(self.hack_code)
        self.hack_code = ''


    def writeArithmetic(self, command): 

        """Define basic arithmetic commands and translate them"""

        unary = {         
            "neg": 'negu',
            "not": 'not'
        }
        binary = {
            "add": 'add',
            "sub": 'sub',
            "and": 'and',
            "or": 'or',
            "eq": 'seq',
            "gt": 'sgt',
            "lt": 'slt'
        }
        command=command.strip()     
        if command in binary:
            self.hack_code += 'addiu $sp,$sp,4\n' #SP--
            self.hack_code += 'lw $t8,0($sp)\n'   #Pop SP and save in t8
            self.hack_code += 'addiu $sp,$sp,4\n'
            self.hack_code += 'lw $t9,0($sp)\n'
            self.hack_code += binary[command] + ' $t8,$t8,$t7\n'
            self.hack_code += 'sw $t9,0($sp)\n'
            self.hack_code += 'subiu $sp,$sp,4\n'
        elif command in unary:
            self.hack_code += 'addiu $sp,$sp,4\n'
            self.hack_code += 'lw $t9,0($sp)\n'
            self.hack_code += unary[command] + ' $t8,$t8\n'
            self.hack_code += 'sw $t9,0($sp)\n'
            self.hack_code += 'subiu $sp,$sp,4\n'
        else:
            print("ERROR: The comando "+str(command) +
                " is not recognized in the arithmetic commands of VM")
            exit(1)

        self.file.write(self.hack_code)
        self.hack_code = ''



    def writePushPop(self, command, segment, index):

        """ Translate the push and pop to hack"""

        initialValue = {
            'local':'$t0',
            'argument':'$t1',
            'this':'$t2',
            'that':'$t3',
            'temp': '$t4',
            'static': '$t5',
            'pointer': '$t6',
            'constant':None,
        }

        if command == 'C_PUSH':    
            if segment == 'constant':
                self.hack_code+='li $t8,' + index + '\n'
                self.hack_code+='sw $t8,0($sp)\n' #Save $t7 in $SP
                self.hack_code+='subiu $sp,$sp,4\n' #SP position -1
            elif segment=='pointer':
                self.hack_code+=()
            else:
                self.hack_code+='lw $t8,' + str(int(index)*4) + '('+initialValue[segment]+')\n'
                self.hack_code+='sw $t8,0($sp)\n'
                self.hack_code+='subiu $sp,$sp,4\n'
        
        elif command =='C_POP':

            if segment=='pointer':
                self.hack_code+=()
            else:
                self.hack_code+='addiu $sp,$sp,4\n'
                self.hack_code+='lw $t8,0($sp)\n'
                self.hack_code+='sw $t8,' + str(int(index)*4) + '('+initialValue[segment]+')\n'

                
        self.file.write(self.hack_code)
        self.hack_code = ''  



    def writeLabel(self,label):

        """Write label following MIPS Language"""

        self.hack_code+=label.strip()+':'+'\n'
        self.file.write(self.hack_code) 
        self.hack_code = ''  




    def writeGoto(self,label):

        """Write Goto to MIPS Language"""

        self.hack_code+='j ' + label.strip() + '\n'
        self.file.write(self.hack_code) 
        self.hack_code = '' 




    def writeIfGoto(self,label):

        """Write the IF Module to MIPS Language"""

        self.hack_code += '\n#if-goto function\n'
        self.hack_code += 'addiu $sp,$sp,4\n' #SP--
        self.hack_code += 'lw $t8,0($sp)\n'
        self.hack_code += 'bge $t8,1,'+label.strip()+'\n' #Greater than 1
        #self.hack_code += 'beq $t8,1,'+label.strip()+'\n'
        self.hack_code += '\n#if-goto end function\n'
        self.file.write(self.hack_code) 
        self.hack_code = ''



    def writeCall(self,function_name,num_of_args):    

        """Write Call Function to MIPS Language"""

        retadd = function_name +'RET'+str(self.call_count)
        self.call_count+=1 

        self.hack_code+=(retadd+':\n') #ESTO PUEDE ESTAR MAL HAY QUE REVISAR

        self.hack_code+=('  sw $t10($sp)\n')# push RetAdress
        self.hack_code+=('  sub $sp,$sp,4\n')

        self.hack_code+=('  sw $t0,0($sp)\n')# push LCL
        self.hack_code+=('  sub $sp,$sp,4\n')
        self.hack_code+=('  sw $t1,0($sp)\n')# push ARG
        self.hack_code+=('  sub $sp,$sp,4\n')
        self.hack_code+=('  sw $t2,0($sp)\n')# push THIS
        self.hack_code+=('  sub $sp,$sp,4\n')
        self.hack_code+=('  sw $t3,0($sp)\n')# push THAT
        self.hack_code+=('  sub $sp,$sp,4\n')

        self.hack_code+=('  move $t0,$sp\n') #LCL = SP
        
        '''
        resta == 5 + numArgs -> ARG = SP - resta
        resta = (numArgs*4)+20
        numArgs * 4 para que sean un espacio de MIPS y 20 que es 54 para que sean los 5 espacios a moverse
        '''
        resta=str((int(num_of_args)*4)+20)
        self.hack_code+=('  subiu $t1,$sp,'+resta+'\n') #ARG = SP - 5 - numArgs

        self.hack_code+=('  j '+function_name+'\n')

        self.file.write(self.hack_code) 
        self.hack_code = ''
             



                
    def writeReturn(self): 

        """Write return in MIPS Assembly Language"""

        self.hack_code+=('\n#return start\n')
        self.hack_code+=('move $t8,$t0\n') # T8 es igual a endFrame = LCL
        self.hack_code+=('addiu $t7,$t8,20\n') # T7 es igual a retAddr
        self.hack_code+=('lw $t7,0($t8)\n') 

        self.textMain+=('add $sp,$sp,4\n')
        self.textMain+=('lw $t9,0($sp)\n') 
        self.textMain+=('sw $t9,0($t1)\n') # ARG = pop (?)

        self.hack_code+=('subiu $sp,$t1,4\n') #SP = ARG + 1
        self.hack_code+=('addiu $t3,$t8,4\n') #THAT = endFrame-1T
        self.hack_code+=('addiu $t2,$t8,8\n') #THIS = endFrame-2
        self.hack_code+=('addiu $t1,$t8,12\n') #ARG = endFrame-3
        self.hack_code+=('addiu $t0,$t8,16\n') #LCL = endFrame-4
        self.hack_code+=('jr $t7\n') #Salta a retAddr
        self.hack_code+=('\n#return end\n')
        self.file.write(self.hack_code) 
        self.hack_code = ''                      




    def writeFunction(self,function_name,num_of_locals):

        """Write Function Name in MIPS Language"""

        self.hack_code+=('\n#function start\n')
        self.hack_code+= function_name.strip()+':\n'
        self.hack_code+='   li $t8,0\n'
        for i in range(int(num_of_locals)):
            self.hack_code+='   subi $sp,$sp,4\n'
            self.hack_code+='   sw $t8,0($sp)\n'
        self.hack_code+=('\n#function end\n')
        self.file.write(self.hack_code) 
        self.hack_code = ''    
            
    


    def closeAll(self):

        """End Function"""

        self.hack_code+='li $v0,10\n'
        self.hack_code+='syscall\n'
        self.file.write(self.hack_code)
        self.hack_code='' 
        self.file.close()  