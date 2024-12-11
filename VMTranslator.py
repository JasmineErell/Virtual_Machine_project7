from CodeWriter import CodeWriter
from parser import Parser

class VMTranslator:
    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path
        with open(self.out_path, "w") as f:
            f.write("")

    def main_loop(self):
        parser = Parser(self.in_path)
        codeWriter = CodeWriter(self.out_path)
        while parser.hasMoreLines():
            parser.advance()
            command = parser.command_type()
            if command == "C_PUSH" or command == "C_POP":
                ##handling pop/push operations
                clean_line = parser.line_cleaner(parser.current_line)
                command = clean_line.split(" ")[0]
                segment = parser.arg1()
                index = parser.arg2()
                codeWriter.WritePushPop(command, segment, index)

            else:
                command = parser.arg1()
                codeWriter.writeArithmetic(command)


