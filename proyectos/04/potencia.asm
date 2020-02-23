// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// R2 = R0 ^ R1
// Initialize the variables
        @R0
        D=M
        @sum      //sum = r0
        M=D
        @j        //j = r0
        M=D
        @result   //result = r0
        M=D     
        @R1
        D=M      
        @FINISH   //r1 = 0, return r2 = 1
        D;JEQ
        @i        //i = r1
        M=D

(LOOP)
        @R0
        D=M
        @j
        M=D
	@sum
	D=M
	@result
	M=D
        @i 
        MD=M-1       // decrementar el contador i
        @FINISHLOOP
        D;JLE

(LOOPSUM)
        @j 
        MD=M-1       // decrementar el contador j
        @LOOP
        D;JLE
        @result
        D=M
        @sum
        M=D+M        // tally the sum 
        @LOOPSUM
        0;JMP
        
(FINISH)
        @R2
        M=1
        @END
        0;JMP

(FINISHLOOP)
        @result
        D=M
        @R2
        M=D
(END)
        @END
        0;JMP
