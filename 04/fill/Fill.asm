// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    @pixel
    M = 0
(LOOP)
    @KBD
    D = M
    @BLACK
    D; JNE
    @CLEAR
    D; JEQ
    @LOOP
    0; JMP
(BLACK)
    @pixel
    D = M
    @8192
    D = D - A
    @END
    D; JEQ
    @SCREEN
    D = M
    @pixel
    D = M
    @SCREEN
    A = A + D
    M = -1
    @pixel
    M = M + 1
    @BLACK
    0; JMP
(CLEAR)
    @pixel
    D = M
    @8192
    D = D - A
    @END
    D; JEQ
    @pixel
    D = M
    @SCREEN
    A = A + D
    M = 0
    @pixel
    M = M + 1
    @CLEAR
    0; JMP
(END)
    @pixel
    M = 0
    @LOOP
    0; JMP
