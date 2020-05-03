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



    def writeArithmetic(self, command): 

        """Define basic arithmetic commands and translate them"""

        unary = {         
            "neg": '-',
            "not": '!'
        }
        binary = {
            "add": '+',
            "sub": '-',
            "and": '&',
            "or": '|'
        }
        jump = {
            "eq": 'JEQ',
            "gt": 'JGT',
            "lt": 'JLT'
        }
        command=command.strip()     
        if command in binary:
            self.hack_code += '@SP\n'     # Top of pile
            self.hack_code += 'M=M-1\n' 
            self.hack_code += 'A=M\n'     # A=M[SP-1]
            self.hack_code += 'D=M\n'     # D=A
            self.hack_code += 'A=A-1\n'
            self.hack_code = self.hack_code+'M=M'+binary[command]+'D\n' # Operation with D Register
        elif command in unary:
            self.hack_code += '@SP\n'     # Top of pile
            self.hack_code += 'A=M-1\n'
            self.hack_code = self.hack_code+'M='+unary[command]+'M\n' 
        elif command in jump:
            self.hack_code += '@SP\n'    # Top of pile
            self.hack_code += 'A=M-1\n' 
            self.hack_code += 'D=M\n'     # Top element saved in D
            self.hack_code =  'D=M-D\n' 
            self.hack_code = self.hack_code+'@BOOL'+str(self.bool_count)+'\n'
            self.hack_code = self.hack_code+'D;'+jump[command]+'\n'
            self.hack_code += '@SP\n'
            self.hack_code += 'A=M-1\n'
            self.hack_code += 'M=0\n'
            self.hack_code = self.hack_code+'@ENDBOOL'+str(self.bool_count)+'\n'
            self.hack_code += '0;JMP\n'
            self.hack_code = self.hack_code+'(BOOL'+str(self.bool_count)+')\n'
            self.hack_code += '@SP\n'
            self.hack_code += 'A=M-1\n'  # Substract 1
            self.hack_code += 'M=-1\n'   # Put it on True
            self.hack_code = self.hack_code+'(ENDBOOL'+str(self.bool_count)+')\n'
            self.bool_count = self.bool_count+1
        else:
            print("ERROR: The comando "+str(command) +
                " is not recognized in the arithmetic commands of VM")
            exit(1)

        self.file.write(self.hack_code)
        self.hack_code = ''



    def writePushPop(self, command, segment, index):

        """ Translate the push and pop to hack"""

        self.find_Destiny(segment,index)
        if command == 'C_PUSH':    
            if segment == 'constant':
                self.hack_code+='D=A\n' # Save value
            else:
                self.hack_code+='D=M\n' # Save value of address
            self.hack_code+=('@SP\n')   # Top of Pile
            self.hack_code+=('A=M\n')   
            self.hack_code+=('M=D\n')   
            self.hack_code+=('@SP\n')   # Increment in SP
            self.hack_code+=('M=M+1\n')
        elif command =='C_POP':
            self.hack_code+='D=A\n'  # Save in D the destiny's direction
            self.hack_code+='@R13\n' # save in R13 D
            self.hack_code+='M=D\n'
            self.hack_code+='@SP\n'   # Top of Pile
            self.hack_code+='AM=M-1\n'
            self.hack_code+='D=M\n'   # Save in D top of pile's
            self.hack_code+='@R13\n'
            self.hack_code+='A=M\n'
            self.hack_code+='M=D\n'   # Save popped value  
        self.file.write(self.hack_code)
        self.hack_code = ''  




    def find_Destiny(self,segment,index):

        """ Find segment of the index """

        try:
            index=int(index)
        except ValueError:
            print("ERROR: index "+index.strip() +" not valid")
            exit(1)  

        InitialValue={
            'local': 'LCL',
            'argument': 'ARG', 
            'this': 'THIS', 
            'that': 'THAT', 
            'pointer': 3, 
            'temp': 5, 
            'static': 16,
            'constant':None 
        }

        try:
            value = InitialValue[segment]
        except(KeyError):
            print("ERROR: Segment "+segment.strip() + " doesn't exist")
            exit(1)

        if segment == 'constant':
           self.hack_code+='@' + str(index)+'\n'
        elif segment == 'static':
            self.hack_code+='@' + self.output_filename + '.' + str(index)+'\n'
        elif segment in ['pointer', 'temp']:
            self.hack_code+='@R' + str(value + int(index))+'\n'
        elif segment in ['local', 'argument', 'this', 'that']: 
            self.hack_code+='@' + value+'\n'
            self.hack_code+='D=M\n'
            self.hack_code+='@' + str(index)+'\n'
            self.hack_code+='A=D+A\n'




    def writeLabel(self,label):

        """Write label following Hack Language"""

        self.hack_code=self.hack_code+'('+ self.output_filename+self.currentFunction+':'+label.upper().strip()+')'+'\n'
        self.file.write(self.hack_code) 
        self.hack_code = ''  




    def writeGoto(self,label):

        """Write Goto to Hack Language"""

        self.hack_code=self.hack_code+'@'+self.output_filename+self.currentFunction+':'+label.upper()+'\n'
        self.hack_code+='0;JMP\n' 
        self.file.write(self.hack_code) 
        self.hack_code = '' 




    def writeIf(self,label):

        """Write the IF Module to Hack Language"""

        self.hack_code+='@SP\n'
        self.hack_code+='AM=M-1\n'    
        self.hack_code+='D=M\n'
        self.hack_code+='A=A-1\n'  
        self.hack_code=self.hack_code+'@'+self.output_filename+self.currentFunction+':'+label.upper()+'\n'
        self.hack_code+='D;JNE\n'     # if !=0 do JUMP
        self.file.write(self.hack_code) 
        self.hack_code = ''

    def writeInit(self):

        """ Write Init to Hack Language"""

        self.hack_code+='@256\n'            # 256 to SP 
        self.hack_code+='D=A\n'
        self.hack_code+='@SP\n'
        self.hack_code+='M=D\n'             
        self.file.write(self.hack_code) 
        self.hack_code=''
        self.writeCall('Sys.init',0)




    def writeCall(self,function_name,num_of_args):    

        """Write Call Function to Hack Language"""

        retadd = function_name +'RET'+str(self.call_count)
        self.call_count+=1 

        self.pushRetAdd(retadd)
        self.writePushPointer('LCL')
        self.writePushPointer('ARG')
        self.writePushPointer('THIS')
        self.writePushPointer('THAT')

        self.hack_code+=('@SP\n')      
        self.hack_code+=('D=M\n')
        self.hack_code+=('@LCL\n')   
        self.hack_code+=('M=D\n')  

        self.hack_code+=('@SP\n')     
        self.hack_code+=('D=M\n')

        vals = str(int(num_of_args)+5)
        self.hack_code+=('@'+vals+'\n')
        self.hack_code+=('D=D-A\n')
        self.hack_code+=('@ARG\n')     
        self.hack_code+=('M=D\n')
        
        self.hack_code+=('@'+function_name.replace(' ','')+'\n')
        self.hack_code+=('0;JMP\n')
        self.hack_code+='('+retadd+')'+'\n'
        self.file.write(self.hack_code) 
        self.hack_code = ''  
             



                
    def writeReturn(self): 

        """Write return in Hack Assembly Language"""

        self.hack_code+=('@LCL\n')
        self.hack_code+=('D=M\n') 
        self.hack_code+=('@R13\n')
        self.hack_code+=('M=D\n')

        self.hack_code+=('@R13\n')
        self.hack_code+=('D=M\n')    
        self.hack_code+=('@5\n')
        self.hack_code+=('D=D-A\n')
        self.hack_code+=('A=D\n')
        self.hack_code+=('D=M\n')  
        self.hack_code+=('@R14\n')
        self.hack_code+=('M=D\n')

        self.hack_code+='@SP\n'   
        self.hack_code+='M=M-1\n' 
        self.hack_code+='A=M\n' 
        self.hack_code+='D=M\n' 
        self.hack_code+=('@ARG\n')   
        self.hack_code+=('A=M\n')
        self.hack_code+=('M=D\n')

        self.hack_code+=('@ARG\n') 
        self.hack_code+=('D=M\n')
        self.hack_code+=('@SP\n') 
        self.hack_code+=('M=D+1\n')

        self.setPointer('THAT','1')  # push THAT
        self.setPointer('THIS','2')  # push THIS
        self.setPointer('ARG','3')   # push ARG
        self.setPointer('LCL','4')   # push LCL

        self.hack_code+=('@R14\n') 
        self.hack_code+=('A=M\n')
        self.hack_code+=('0;JMP\n')
        self.file.write(self.hack_code) 
        self.hack_code = ''                        




    def setPointer(self,variable,index):

        """Set pointer function to Hack"""

        self.hack_code+=('@R13\n') 
        self.hack_code+=('D=M\n')
        self.hack_code+=('@'+index+'\n')
        self.hack_code+=('D=D-A\n')
        self.hack_code+=('A=D\n')
        self.hack_code+=('D=M\n')
        self.hack_code+=('@'+variable+'\n')    
        self.hack_code+=('M=D\n')

    

    def writePushPointer(self,value):

        """ Translate Push Pointer to Hack"""

        self.hack_code+=('@'+value+'\n')
        self.hack_code+=('D=M\n')
        self.hack_code+=('@SP\n')
        self.hack_code+=('A=M\n')
        self.hack_code+=('M=D\n')
        self.hack_code+=('@SP\n')
        self.hack_code+=('M=M+1\n')




    def pushRetAdd(self,ret):

        """Push return address"""

        self.hack_code+=('@'+ret+'\n')
        self.hack_code+=('D=A\n')
        self.hack_code+=('@SP\n') 
        self.hack_code+=('A=M\n') 
        self.hack_code+=('M=D\n')
        self.hack_code+=('@SP\n')   
        self.hack_code+=('M=M+1\n')



    def writeFunction(self,function_name,num_of_locals):

        """Write Function Name in Hack Assemply Language"""

        self.currentFunction=function_name
        self.hack_code+=('('+function_name.replace(" ", "")+')'+'\n')
        for x in range(int(num_of_locals)):
            self.hack_code+=('D=0\n')
            self.hack_code+=('@SP\n') 
            self.hack_code+=('A=M\n') 
            self.hack_code+=('M=D\n')  
            self.hack_code+=('@SP\n')   
            self.hack_code+=('M=M+1\n')
        
        self.file.write(self.hack_code) 
        self.hack_code = ''    
            
    


    def closeAll(self):

        """End Function"""

        self.hack_code+='(END)\n'
        self.hack_code+='@END\n'
        self.hack_code+='0;JMP\n'
        self.file.write(self.hack_code)
        self.hack_code='' 
        self.file.close()  