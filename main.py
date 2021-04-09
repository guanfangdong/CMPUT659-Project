import numpy as np
from DSL_Str import *
from read_sl import ReadSL


class BUS():
    def __init__(self, bound, str, int, str_var, int_var, io_list):
        self.bound = bound
        self.str = [Str(i) for i in str]
        self.int = [Int(i) for i in int]
        self.str_var = [StrVar(i) for i in str_var]
        self.int_var = [IntVar(i) for i in int_var]
        self.bool = [Bool(True), Bool(False)]
        self.io_list = io_list
        self.bank = self.str + self.int + self.bool + self.str_var + self.int_var
        print([i.toString() for i in self.bank])

    def gen_p_one_arg(self, p, type):
        new_progs = []
        if type is "S":
            for dsl in [Str2Int, Length]:
                new_progs.append(dsl(p))
        elif type is "I":
            new_progs.append(Int2Str(p))
        return new_progs

    def gen_p_two_args(self, left, right, l_type, r_type):
        new_progs = []
        if l_type is "S" and r_type is "S":
            for dsl in [Concat, Contain, Suffixof, Prefixof]:
                new_progs.append(dsl(left, right))
        elif l_type is "S" and r_type is "I":
            new_progs.append(At(left, right))
        elif l_type is "I" and r_type is "I":
            for dsl in [Equal, Plus, Minus]:
                new_progs.append(dsl(left, right))
        return new_progs

    def gen_p_three_args(self, left, mid, right, l_type,
                         m_type, r_type):
        new_progs = []
        arrg = l_type + m_type + r_type
        if arrg is "SSS":
            new_progs.append(Replace(left, mid, right))
        elif arrg is "SII":
            new_progs.append(Substr(left, mid, right))
        elif arrg is "BSS":
            new_progs.append(IteStr(left, mid, right))
        elif arrg is "BII":
            new_progs.append(IteInt(left, mid, right))
        elif arrg is "SSI":
            new_progs.append(IndexOf(left, mid, right))

    def append_helper(self, old_list, new_list):
        if new_list is not None:
            for i in new_list:
                old_list.append(i)

    def grow(self):
        new_progs = []
        for trav_1 in self.bank:
            type_1 = get_type(trav_1)
            self.append_helper(new_progs, self.gen_p_one_arg(trav_1, type_1))
            for trav_2 in self.bank:
                type_2 = get_type(trav_2)
                self.append_helper(new_progs, self.gen_p_two_args(
                    trav_1, trav_2, type_1, type_2))
                for trav_3 in self.bank:
                    type_3 = get_type(trav_3)
                    self.append_helper(new_progs, self.gen_p_three_args(
                        trav_1, trav_2, trav_3,
                        type_1, type_2, type_3))
        return new_progs


    def synthesize(self, debug):
        for level in range(self.bound):
            print("current level is %d" % level)
            new_progs = self.grow()
            for p in new_progs:
                try:
                    io_len = len(self.io_list)
                    for io in self.io_list:
                        result = p.interpret(io)
                        # if debug:
                        #     print(p.toString())
                        #     print(result)
                        if result == io["out"]:
                            io_len -= 1
                    if io_len < len(self.io_list):
                        print("partial solution or solution found:",
                            p.toString())
                    self.bank.append(p)
                except:
                    if debug:
                        print("broken program found:", p.toString())
                    pass
            print("current bank length", len(self.bank))


if __name__ == "__main__":
    f = ReadSL("2171308.sl")
    str_var, str, int_var, int, input, output = f.get_attrs()
    bound = 3
    io_list = []

    for step, i in enumerate(input):
        io_pairs = {}
        for arg_index, arg in enumerate(str_var):
            io_pairs[arg] = i
        io_pairs["out"] = output[step]
        io_list.append(io_pairs)

    solver = BUS(bound, str, int, str_var, int_var, io_list)
    solver.synthesize(debug=True)
