//FibonacciSeries
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=A
@1
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@0
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@1
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@0
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
(main$MAIN_LOOP_START)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@main$COMPUTE_ELEMENT
D;JNE
@main$END_PROGRAM
0;JMP
(main$COMPUTE_ELEMENT)
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M+D
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@2
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@THIS
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M+D
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=A
@1
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@0
A=D+A
D=A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@main$MAIN_LOOP_START
0;JMP
(main$END_PROGRAM)