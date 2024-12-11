from pconst import const

const.C_PUSH = "C_PUSH"
const.C_POP = "C_POP"
const.C_ARITHMETIC = "C_ARITHMETIC"

class Parser(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path)
        self.lts_lines = self.file.readlines()
        self.current_line = None
        self.clean_line_pos = 0
        self.pos = 0

    def line_cleaner(self, string):
        """
        Cleans comments and whitespace from a line
        """
        if type(string) == "NoneType":
            return " "
        else:
            return string.split("//")[0].strip()

    def hasMoreLines(self):
        # Checks if there are more lines to process
        return self.pos < len(self.lts_lines)

    def advance(self):
        while self.hasMoreLines():
            raw_line = self.lts_lines[self.pos]  # Read the next line
            current_line = self.line_cleaner(raw_line)  # Clean the line
            self.pos +=1
            # if current_line and self.instructionType()!= "L_INSTRUCTION":  # Return the first non-empty, cleaned line
            if current_line:
                self.clean_line_pos +=1
                self.current_line = current_line
                return
        self.current_line = None  # Set to None if no valid lines are found

    def command_type(self):
        """
        This function will operate on current line in the vm file.
        :return: the type of command in this line
        """
        clean_line = self.line_cleaner(self.current_line)
        if (clean_line.split(" ")[0] == "push"):
            return const.C_PUSH
        if (clean_line.split(" ")[0] == "pop"):
            return const.C_POP
        else:
            return const.C_ARITHMETIC

    def arg1(self):
        """
        The function gets a line in VM file, cleans it and get the putput
        :return:
        If it's an arithmetic op - the line itself
        If it's pop or push - the destination
        """
        clean_line = self.line_cleaner(self.current_line)
        if (self.command_type() == const.C_ARITHMETIC):
            return clean_line
        else:
            return clean_line.split(" ")[1]

    def arg2(self):
        """
               The function gets a line in VM file, cleans it and get the putput
               :return:
               If it's an arithmetic op - the line itself
               If it's pop or push - the subject that we are popping or pushing
               """
        clean_line = self.line_cleaner(self.current_line)
        if (self.command_type() == const.C_ARITHMETIC):
            return clean_line
        else:
            return clean_line.split(" ")[2]




