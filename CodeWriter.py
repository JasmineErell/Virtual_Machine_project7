from parser import Parser
class CodeWriter:
    def __init__(self, out_path):
        self.out_path = out_path

    def WritePushPop(self, command, segment, index):
        with open(self.out_path, "w", newline='\n') as f:
            if (command == "C_PUSH"):

                if segment == "constant":
                    f.write("// D = " + index)
                    f.write("@" + index)
                    f.write("D=A")
                    f.write("// RAM[SP] = " + index)
                    f.write("@SP")
                    f.write("A=M")
                    f.write("M=D")
                    f.write("//SP++")
                    f.write("@SP")
                    f.write("M=M+1")
                # NOT SURE IF WE WILL NEED IT?
                # if (command == "C_POP"):
                #     f.write("// SP--")
                #     f.write("@SP")
                #     f.write("M=M-1")
                #     f.write("Stor the popped value in to D")
                #     f.write("A=M")
                #     f.write("D=M")
                #     f.write()
                else:
                    f.write("//Load the index " + index)
                    f.write("@" + index)
                    f.write("D=A")
                    f.write("//Base address of the " + segment + " segment")
                    f.write("@" + segment)
                    f.write("A=M")
                    f.write("A=A+D")
                    f.write("D=M")
                    f.write("//Accesses the stack pointer")
                    f.write("A=M")
                    f.write("//RAM[SP] = D")
                    f.write("M=D")
                    f.write("//SP pointer +=1")
                    f.write("@SP")
                    f.write("M=M+1")






        return True
