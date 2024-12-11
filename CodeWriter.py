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
            "static": (self.out_path.split("/")[-1]).split(".")[0]
        }
        self.label_counter = 0  # For unique labels in comparison operations

    def writeArithmetic(self, command):
        """Writes assembly code for arithmetic-logical VM command"""
        with open(self.out_path, "a", newline='\n') as f:
            f.write("//" + command + "\n")
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
            f.write("//" + command + " " + segment + " " + index + "\n")
            if command == "push":
                ## Push operations takes the value stored in RAM and push it into SP
                if segment == "constant":
                    f.write("@" + index + "\n")
                    f.write("D=A\n")
                    f.write("@SP\n")
                    f.write("A=M\n")
                    f.write("M=D\n")
                    f.write("@SP\n")
                    f.write("M=M+1\n")

                elif segment == "pointer":
                    if index == 0: ##Push pointer 0
                        f.write("@THIS\n")
                        f.write("D=M\n")
                        f.write("@SP\n")
                        f.write("A=M\n")
                        f.write("M=D\n")
                        f.write("@SP\n")
                        f.write("M=M+1\n")
                    elif index == 1: ##Push pointer 1
                        f.write("@THAT\n")
                        f.write("D=M\n")
                        f.write("@SP\n")
                        f.write("A=M\n")
                        f.write("M=D\n")
                        f.write("@SP\n")
                        f.write("M=M+1\n")

                elif segment == "static":
                    f.write("@" + self.segment_table.get(segment) + "." + index + "\n")
                    f.write("D=M\n")
                    f.write("@SP\n")
                    f.write("A=M\n")
                    f.write("M=D\n")
                    f.write("@SP\n")
                    f.write("M=M+1\n")

                else:
                    ##Segments witch are not const, pointer, or static - takes the value @X from the table
                    f.write("@" + str(index) + "\n")
                    f.write("D=A\n")
                    f.write("@" + self.segment_table.get(segment) + "\n")
                    f.write("A=M+D\n")
                    f.write("D=M\n")
                    f.write("@SP\n")
                    f.write("A=M\n")
                    f.write("M=D\n")
                    f.write("@SP\n")
                    f.write("M=M+1\n")

            if command == "pop":
                ##Pop commands removes a value from the head of stack, and store it in RAM
                if segment == "pointer":
                    if index == 0:
                        f.write("@SP\n")
                        f.write("AM=M-1\n")
                        f.write("D=M\n")
                        f.write("@THIS\n")
                        f.write("M=D\n")
                    if index == 1:
                        f.write("@SP\n")
                        f.write("AM=M-1\n")
                        f.write("D=M\n")
                        f.write("@THAT\n")
                        f.write("M=D\n")

                elif segment == "static":
                    f.write("@SP\n")
                    f.write("AM=M-1\n")
                    f.write("D=M\n")
                    f.write("@" + self.segment_table.get(segment) + "." + index + "\n")
                    f.write("M=D\n")

                else:
                    #Poping commands that are not pointers
                    f.write("@" + self.segment_table.get(segment) + "\n") #@segment
                    f.write("D=M\n")
                    f.write("@" + str(index) + "\n") #@index
                    f.write("D=D+A\n") #D= segment+index
                    f.write("@R13\n")
                    f.write("M=D\n")
                    f.write("@SP\n")
                    f.write("AM=M-1\n")
                    f.write("D=M\n")
                    f.write("@R13\n")
                    f.write("A=M\n")
                    f.write("M=D\n")


