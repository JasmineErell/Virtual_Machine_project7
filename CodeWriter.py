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
        self.label_counter = 0  # For unique labels in comparison operations

    def writeArithmetic(self, command):
        """Writes assembly code for arithmetic-logical VM command"""
        with open(self.out_path, "a", newline='\n') as f:
            if command == "add":
                # Pop two values and add them
                f.write("@SP\n")  # Get stack pointer
                f.write("AM=M-1\n")  # Decrement SP and get address
                f.write("D=M\n")  # D = y
                f.write("A=A-1\n")  # Point to x
                f.write("M=D+M\n")  # x + y

            elif command == "sub":
                # Pop two values and subtract
                f.write("@SP\n")  # Get stack pointer
                f.write("AM=M-1\n")  # Decrement SP and get address
                f.write("D=M\n")  # D = y
                f.write("A=A-1\n")  # Point to x
                f.write("M=M-D\n")  # x - y

            elif command == "neg":
                # Negate top value
                f.write("@SP\n")  # Get stack pointer
                f.write("A=M-1\n")  # Point to top of stack
                f.write("M=-M\n")  # Negate value

            elif command in ["eq", "gt", "lt"]:
                # Compare top two values
                label_true = f"{command}true{self.label_counter}"
                label_end = f"{command}end{self.label_counter}"
                self.label_counter += 1

                comparison = {
                    "eq": "JEQ",
                    "gt": "JGT",
                    "lt": "JLT"
                }[command]

                f.write("@SP\n")  # Get stack pointer
                f.write("AM=M-1\n")  # Decrement SP and get address
                f.write("D=M\n")  # D = y
                f.write("A=A-1\n")  # Point to x
                f.write("D=M-D\n")  # D = x - y
                f.write(f"@{label_true}\n")
                f.write(f"D;{comparison}\n")  # Jump if comparison true
                f.write("@SP\n")  # False case
                f.write("A=M-1\n")
                f.write("M=0\n")  # Push false (0)
                f.write(f"@{label_end}\n")
                f.write("0;JMP\n")  # Skip true case
                f.write(f"({label_true})\n")
                f.write("@SP\n")  # True case
                f.write("A=M-1\n")
                f.write("M=-1\n")  # Push true (-1)
                f.write(f"({label_end})\n")

            elif command == "and":
                f.write("@SP\n")  # Get stack pointer
                f.write("AM=M-1\n")  # Decrement SP and get address
                f.write("D=M\n")  # D = y
                f.write("A=A-1\n")  # Point to x
                f.write("M=D&M\n")  # x AND y

            elif command == "or":
                f.write("@SP\n")  # Get stack pointer
                f.write("AM=M-1\n")  # Decrement SP and get address
                f.write("D=M\n")  # D = y
                f.write("A=A-1\n")  # Point to x
                f.write("M=D|M\n")  # x OR y

            elif command == "not":
                f.write("@SP\n")  # Get stack pointer
                f.write("A=M-1\n")  # Point to top of stack
                f.write("M=!M\n")  # NOT x
    def WritePushPop(self, command, segment, index):
        with open(self.out_path, "a", newline='\n') as f:
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
                    f.write("//Compute the address " + self.segment_table.get(segment) + "+ " + str(index) + "and store it in R13 temporally\n")
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

# # Test function for WritePushPop
# test = CodeWriter("C:/secondYear/Nand2Tetris/res.asm")
# test.WritePushPop("push", "local", 10)