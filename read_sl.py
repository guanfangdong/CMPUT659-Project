# This repository is for project of CMPUT 659 in University of Alberta. 
# The owners are Guanfang Dong and Jiaqi He.
# For CMPUT 659 students, you should not copy any of code from our work.

class ReadSL():
    """
    input: file address
    output: call method get_attrs to get following variables
            str_var: variables to represent input data
            str: initial string that used in DSL
            int_var: variables to represent input int data
            int: initial int that used in DSL
            input: input string database
            output: output string database
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.str_var = []
        self.str = []
        self.int_var = []
        self.int = []
        self.input = []
        self.output = []
        self.read()

    def parse_line(self, line):
        if "constraint" in line:
            indicies = [i for i, x in enumerate(line) if x == '"']
            input = line[indicies[0]+1:indicies[1]]
            try:
                output = line[indicies[2]+1:indicies[3]]
            except:
                right = line.split(")")
                right = right[-3]
                try:
                    output = int(right)
                except:
                    if 'true' in right:
                        output = True
                    elif 'false' in right:
                        output = False
            self.input.append(input)
            self.output.append(output)
        else:
            lines = line.split(" ")
            try:
                self.int = [int(i) for i in lines]
            except:
                if "arg" in lines[0]:
                    self.str_var = lines
                else:
                    indicies = [i for i, x in enumerate(line) if x == '"']
                    for i in range(0, len(indicies), 2):
                        self.str.append(line[indicies[i]+1:indicies[i+1]])

    def read(self):
        f = open(self.file_name, "r")
        lines = f.readlines()
        for step, line in enumerate(lines):
            
            if "ntString String" in line:
                str_var = lines[step + 1].strip()
                str = lines[step + 2].strip()
            if "ntInt Int" in line:
                int_var = lines[step + 1].strip()
                if int_var != "":
                    raise Exception
                int = lines[step + 2].strip()
            if "constraint" in line:
                io_pair = line.strip()
                self.parse_line(io_pair)
        for i in [str_var, str, int_var, int]:
            self.parse_line(i)

    def get_attrs(self):
        return self.str_var, self.str, self.int_var, \
            self.int, self.input, self.output

if __name__ == "__main__":
    f = ReadSL("11440431.sl")
    print(f.get_attrs())
