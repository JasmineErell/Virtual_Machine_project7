import os

class CodeWriter:
    def __init__(self,out_path):
        self.out_path = out_path
        self.segment_table = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "TMP",
        }

    def WritePushPop(self, command, segment, index):
        with open(self.out_path, "w", newline='\n') as f:
            if command == "push":
                ## Push operations takes the value stored in RAM and push it into SP
                if segment == "constant":
                    f.write("// D = " + index + "\n")
                    f.write("@" + index + "\n")
                    f.write("D=A\n")
                    f.write("// RAM[SP] = " + index + "\n")
                    f.write("@SP\n")
                    f.write("A=M\n")
                    f.write("M=D\n")
                    f.write("//SP++\n")
                    f.write("@SP\n")
                    f.write("M=M+1\n")

                elif segment == "pointer":
                    if index == 0: ##Push pointer 0
                        f.write("//Access the THIS register (RAM[3])\n")
                        f.write("@THIS\n")
                        f.write("D=M\n")
                        f.write("@SP\n")
                        f.write("A=M\n")
                        f.write("M=D\n")
                        f.write("//SP ++\n")
                        f.write("@SP\n")
                        f.write("M=M+1\n")
                    elif index == 1: ##Push pointer 1
                        f.write("//Access the THIS register (RAM[3])\n")
                        f.write("@THAT\n")
                        f.write("D=M\n")
                        f.write("@SP\n")
                        f.write("A=M\n")
                        f.write("M=D\n")
                        f.write("//SP ++\n")
                        f.write("@SP\n")
                        f.write("M=M+1\n")

                else:
                    ##Segments witch are not const or pointer - takes the value @X from the table
                    f.write("//Load the index " + str(index) + "\n")
                    f.write("@" + str(index) + "\n")
                    f.write("D=A\n")
                    f.write("//Base address of the " + segment + " segment\n")
                    f.write("@" + self.segment_table.get(segment) + "\n")
                    f.write("A=M+D\n")
                    f.write("//Insert into D the value of " + self.segment_table.get(segment) + " " + str(index) + "\n")
                    f.write("D=M\n")
                    f.write("//RAM[SP] = D\n")
                    f.write("@SP\n")
                    f.write("A=M\n")
                    f.write("M=D\n")
                    f.write("//SP ++\n")
                    f.write("@SP\n")
                    f.write("M=M+1\n")

            if command == "pop":
                ##Pop commands removes a value from the head of stack, and store it in RAM
                if segment == "pointer":
                    if index == 0:
                        f.write("//Access the SP, store its value in @THIS and decrement SP by 1\n")
                        f.write("@SP\n")
                        f.write("AM=M-1\n")
                        f.write("D=M\n")
                        f.write("@THIS\n")
                        f.write("M=D\n")
                    if index == 1:
                        f.write("//Access the SP, store its value in @THAT and decrement SP by 1\n")
                        f.write("@SP\n")
                        f.write("AM=M-1\n")
                        f.write("D=M\n")
                        f.write("@THAT\n")
                        f.write("M=D\n")
                else:
                    #Poping commands that are not pointers
                    f.write("//Compute the address " + self.segment_table.get(segment)  + "+ " + str(index) + "and store it in R13 temporally\n")
                    f.write("@" + self.segment_table.get(segment) + "\n") #@segment
                    f.write("D=M\n")
                    f.write("@" + str(index) + "\n") #@index
                    f.write("D=D+A\n") #D= segment+index
                    f.write("//Store the relevant address inside R13\n")
                    f.write("@R13\n")
                    f.write("M=D\n")
                    f.write("//Pop the top of the stack:\n")
                    f.write("//First we store in D the value of SP and decrement SP by 1\n")
                    f.write("@SP\n")
                    f.write("AM=M-1\n")
                    f.write("D=M\n")
                    f.write("//Second we take the popped value and store it in the wanted address\n")
                    f.write("@R13\n")
                    f.write("A=M\n")
                    f.write("M=D\n")

# Test function for WritePushPop
test = CodeWriter("C:/secondYear/Nand2Tetris/res.asm")
test.WritePushPop("push", "local", 10)