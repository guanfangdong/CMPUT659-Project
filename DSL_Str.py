# This repository is for project of CMPUT 659 in University of Alberta.
# The owners are Guanfang Dong and Jiaqi He.
# For CMPUT 659 students, you should not copy any of code from our work.

import copy
import re


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def get_type(c):
    """
    Input: DSL program
    Output: str: its type reprsented by "S", "B", "I"
                means "String", "Boolean", "Int" respectively
    """
    for i in [Str, StrVar, Replace, Concat, Substr,
              IteStr, Int2Str, At]:
        if isinstance(c, i):
            return "S"
    for i in [Bool, Equal, Contain, Suffixof, Prefixof]:
        if isinstance(c, i):
            return "B"
    for i in [Int, IntVar, Str2Int, Plus, Minus,
              Length, IteInt, IndexOf]:
        if isinstance(c, i):
            return "I"


def get_symbol(c):
    """
    Input: DSL program
    Output: str: its type reprsented by "S", "B", "I"
                means "String", "Boolean", "Int" respectively
    """
    for i in [Str, StrVar, Replace, Concat, Substr,
              IteStr, Int2Str, At]:
        if c is i:
            return "S"
    for i in [Bool, Equal, Contain, Suffixof, Prefixof]:
        if c is i:
            return "B"
    for i in [Int, IntVar, Str2Int, Plus, Minus,
              Length, IteInt, IndexOf]:
        if c is i:
            return "I"


def get_nodes(sign):
    s = [Str, StrVar, Replace, Concat, Substr,
         IteStr, Int2Str, At]
    b = [Bool, Equal, Contain, Suffixof, Prefixof]
    i = [Int, IntVar, Str2Int, Plus, Minus,
         Length, IteInt, IndexOf]
    if sign == "S":
        return s
    elif sign == "B":
        return b
    elif sign == "I":
        return i
    elif sign == "A":
        return s + b + i


def get_node_str(c):
    str_s = ["Str", "StrVar", "Replace", "Concat", "Substr",
             "IteStr", "Int2Str", "At", "Bool", "Equal",
             "Contain", "Suffixof", "Prefixof", "Int", "IntVar",
             "Str2Int", "Plus", "Minus", "Length", "IteInt", "IndexOf"]

    node = [Str, StrVar, Replace, Concat, Substr,
            IteStr, Int2Str, At, Bool, Equal,
            Contain, Suffixof, Prefixof, Int, IntVar,
            Str2Int, Plus, Minus, Length, IteInt, IndexOf]

    for step, i in enumerate(node):
        if c is i:
            return str_s[step]


def get_type_str(c):
    str_s = ["Str", "StrVar", "Replace", "Concat", "Substr",
             "IteStr", "Int2Str", "At", "Bool", "Equal",
             "Contain", "Suffixof", "Prefixof", "Int", "IntVar",
             "Str2Int", "Plus", "Minus", "Length", "IteInt", "IndexOf"]

    node = [Str, StrVar, Replace, Concat, Substr,
            IteStr, Int2Str, At, Bool, Equal,
            Contain, Suffixof, Prefixof, Int, IntVar,
            Str2Int, Plus, Minus, Length, IteInt, IndexOf]

    for step, i in enumerate(node):
        if isinstance(c, i):
            return str_s[step]


def check_type(c):
    node = [Str, StrVar, Replace, Concat, Substr,
            IteStr, Int2Str, At, Bool, Equal,
            Contain, Suffixof, Prefixof, Int, IntVar,
            Str2Int, Plus, Minus, Length, IteInt, IndexOf]
    for i in node:
        if isinstance(c, i):
            return i


def get_str_names():
    str_s = ["Str", "StrVar", "Replace", "Concat", "Substr",
             "IteStr", "Int2Str", "At", "Bool", "Equal",
             "Contain", "Suffixof", "Prefixof", "Int", "IntVar",
             "Str2Int", "Plus", "Minus", "Length", "IteInt", "IndexOf"]
    return str_s


def get_keys():
    node = [Replace, Concat, Substr,
            IteStr, Int2Str, At, Equal,
            Contain, Suffixof, Prefixof,
            Str2Int, Plus, Minus, Length, IteInt, IndexOf]
    return node


def get_dsl_num(d):
    has_one = [Int2Str, Str2Int, Length]
    has_two = [Concat, At, Equal, Contain, Suffixof, Prefixof,
               Plus, Minus]
    has_three = [Replace, Substr, IteInt, IteStr, IndexOf]
    if d in has_one:
        return 1
    elif d in has_two:
        return 2
    elif d in has_three:
        return 3

def get_content_types(d):
    ss_type = [Concat, Contain, Suffixof, Prefixof]
    sss_type = [Replace]
    sii_type = [Substr]
    bss_type = [IteStr]
    i_type = [Int2Str]
    si_type = [At]
    ii_type = [Equal, Plus, Minus]
    s_type = [Str2Int, Length]
    bii_type = [IteInt]
    ssi_type = [IndexOf]
    
    map_list = ["SS", "SSS", "SII", "BSS", "I", "SI", "II", 
                "S", "BII", "SSI"]
    ALL_types = [ss_type, sss_type, sii_type, bss_type, i_type,
                    si_type, ii_type, s_type, bii_type, ssi_type]
    for step, i in enumerate(ALL_types):
        for j in i:
            if d is j:
                return list(map_list[step])



def init_probe(str_, strval, int_, bool_):
    all_nodes = get_keys()
    probe_dict = {}
    for i in all_nodes:
        probe_dict[i] = 0
    for i in str_ + strval + int_ + bool_:
        probe_dict[i] = 0
    dict_key = list(probe_dict.keys())
    dict_len = len(dict_key)
    for i in dict_key:
        probe_dict[i] = 1/dict_len
    return probe_dict


def init_phog_probe(str_, strval, int_, bool_):

    s = get_nodes("S")
    b = get_nodes("B")
    int = get_nodes("I")

    s_len, b_len, i_len = len(s), len(b), len(int)

    phog_probe = {}

    repl_dict = {}
    conc_dict = {}
    contain_dict = {}
    suff_dict = {}
    pref_dict = {}
    substr_dict = {}
    itestr_dict = {}
    int2str_dict = {}
    at_dict = {}
    equal_dict = {}
    plus_dict = {}
    minus_dict = {}
    str2int_dict = {}
    length_dict = {}
    iteint_dict = {}
    indexof_dict = {}

    for i in s:
        for j in s:
            for k in s:
                repl_dict[(i, j, k)] = 0

    for i in s:
        for j in s:
            conc_dict[(i, j)] = 0
            contain_dict[(i, j)] = 0
            suff_dict[(i, j)] = 0
            pref_dict[(i, j)] = 0

    for each_s in s:
        for j in int:
            for k in int:
                substr_dict[(each_s, j, k)] = 0

    for i in b:
        for j in s:
            for k in s:
                itestr_dict[(i, j, k)] = 0

    for each_i in int:
        int2str_dict[(each_i)] = 0

    for each_s in s:
        for j in int:
            at_dict[(each_s, j)] = 0

    for each_i_1 in int:
        for each_i_2 in int:
            equal_dict[(each_i_1, each_i_2)] = 0
            plus_dict[(each_i_1, each_i_2)] = 0
            minus_dict[(each_i_1, each_i_2)] = 0

    for i in s:
        str2int_dict[(i)] = 0
        length_dict[(i)] = 0

    for each_b in b:
        for j in int:
            for k in int:
                iteint_dict[(each_b, j, k)] = 0

    for each_s in s:
        for j in s:
            for k in int:
                indexof_dict[(each_s, j, k)] = 0

    phog_probe[Replace] = repl_dict
    phog_probe[Concat] = conc_dict
    phog_probe[Contain] = contain_dict
    phog_probe[Suffixof] = suff_dict
    phog_probe[Prefixof] = pref_dict
    phog_probe[Substr] = substr_dict
    phog_probe[IteStr] = itestr_dict
    phog_probe[Int2Str] = int2str_dict
    phog_probe[At] = at_dict
    phog_probe[Equal] = equal_dict
    phog_probe[Plus] = plus_dict
    phog_probe[Minus] = minus_dict
    phog_probe[Str2Int] = str2int_dict
    phog_probe[Length] = length_dict
    phog_probe[IteInt] = iteint_dict
    phog_probe[IndexOf] = indexof_dict
    for i in str_ + strval + int_ + bool_:
        phog_probe[i] = {(i): 0}

    num = 0
    for i in phog_probe.keys():
        num += len(phog_probe[i].keys())

    for i in phog_probe.keys():
        for j in phog_probe[i].keys():
            phog_probe[i][j] = 1/num

    return phog_probe


class Node:
    def getSize(self):
        return self.size

    def toString(self):
        raise Exception('Unimplemented method: toString')

    def interpret(self):
        raise Exception('Unimplemented method: interpret')


class Str(Node):
    def __init__(self, value):
        self.value = value

    def toString(self):
        return self.value

    def interpret(self, env):
        return self.value


class StrVar(Node):
    def __init__(self, name):
        self.value = name

    def toString(self):
        return self.value

    def interpret(self, env):
        return copy.deepcopy(env[self.value])


class Concat(Node):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toString(self):
        return 'concat(' + self.x.toString() + ", " + self.y.toString() + ")"

    def interpret(self, env):
        return self.x.interpret(env) + self.y.interpret(env)


class Replace(Node):
    def __init__(self, input_str, old, new):
        self.str = input_str
        self.old = old
        self.new = new

    def toString(self):
        return self.str.toString() + '.replace(' + self.old.toString() + ", " + self.new.toString() + ")"

    def interpret(self, env):
        return self.str.interpret(env).replace(self.old.interpret(env), self.new.interpret(env), 1)


class Substr(Node):
    def __init__(self, input_str, start, end):
        self.str = input_str
        self.start = start
        self.end = end

    def toString(self):
        return "%s.Substr(%s, %s)" % (self.str.toString(), self.start.toString(), self.end.toString())

    def interpret(self, env):
        return self.str.interpret(env)[self.start.interpret(env): self.end.interpret(env)]


class IteStr(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case

    def toString(self):
        return "(if" + self.condition.toString() + " then " + self.true_case.toString() + " else " + self.false_case.toString() + ")"

    def interpret(self, env):
        if self.condition.interpret(env):
            assert isinstance(self.true_case.interpret(env), str)
            return self.true_case.interpret(env)
        else:
            assert isinstance(self.false_case.interpret(env), str)
            return self.false_case.interpret(env)


class Int2Str(Node):
    def __init__(self, input_int):
        self.int = input_int

    def toString(self):
        return "%s.Int2Str()" % self.int.toString()

    def interpret(self, env):
        return str(self.int.interpret(env))


class At(Node):
    def __init__(self, input_str, pos):
        self.str = input_str
        self.pos = pos

    def toString(self):
        return "%s.At(%s)" % (self.str.toString(), self.pos.toString())

    def interpret(self, env):
        return self.str.interpret(env)[self.pos.interpret(env)]


class Bool(Node):
    def __init__(self, bool):
        self.bool = True if bool == True else False

    def toString(self):
        return str(self.bool)

    def interpret(self, env):
        return self.bool


class Equal(Node):
    def __init__(self, int_left, int_right):
        self.int_left = int_left
        self.int_right = int_right

    def toString(self):
        return "Equal(%s, %s)" % (self.int_left.toString(), self.int_right.toString())

    def interpret(self, env):
        return True if self.int_left.interpret(env) == self.int_right.interpret(env) else False


class Contain(Node):
    def __init__(self, input_str, item):
        self.str = input_str
        self.item = item

    def toString(self):
        return "%s.Contain(%s)" % (self.str.toString(), self.item.toString())

    def interpret(self, env):
        return True if self.item.interpret(env) in self.str.interpret(env) else False


class Suffixof(Node):
    def __init__(self, input_str, item):
        self.str = input_str
        self.item = item

    def toString(self):
        return "%s.Suffixof(%s)" % (self.str.toString(), self.item.toString())

    def interpret(self, env):
        return True if self.str.interpret(env).endswith(self.item.interpret(env)) else False


class Prefixof(Node):
    def __init__(self, input_str, item):
        self.str = input_str
        self.item = item

    def toString(self):
        return "%s.Prefixof(%s)" % (self.str.toString(), self.item.toString())

    def interpret(self, env):
        return True if self.str.interpret(env).startswith(self.item.interpret(env)) else False


class Int(Node):
    def __init__(self, value):
        self.value = value

    def toString(self):
        return str(self.value)

    def interpret(self, env):
        return self.value


class IntVar(Node):
    def __init__(self, name):
        self.value = name

    def toString(self):
        return self.value

    def interpret(self, env):
        return copy.deepcopy(env[self.value])


class Str2Int(Node):
    def __init__(self, input_str):
        self.str = input_str

    def toString(self):
        return "%s.Str2Int()" % self.str.toString()

    def interpret(self, env):
        return int(self.str.interpret(env))


class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " + " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)


class Minus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " - " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) - self.right.interpret(env)


class Length(Node):
    def __init__(self, input_str):
        self.str = input_str

    def toString(self):
        return "%s.Length()" % self.str.toString()

    def interpret(self, env):
        return len(self.str.interpret(env))


class IteInt(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case

    def toString(self):
        return "(if" + self.condition.toString() + " then " + self.true_case.toString() + " else " + self.false_case.toString() + ")"

    def interpret(self, env):
        if self.condition.interpret(env):
            assert isinstance(self.true_case.interpret(env), int)
            return self.true_case.interpret(env)
        else:
            assert isinstance(self.false_case.interpret(env), int)
            return self.false_case.interpret(env)


class IndexOf(Node):
    def __init__(self, input_str, item, start):
        self.input_str = input_str
        self.item = item
        self.start = start

    def toString(self):
        return "%s.IndexOf(%s, %s)" % (self.input_str.toString(), self.item.toString(), self.start.toString())

    def interpret(self, env):
        return self.input_str.interpret(env)[self.start.interpret(env):].index(self.item.interpret(env))


class GetInside():
    def __init__(self):
        self.parent = []
        self.child = []
        self.size = 0

    def get_parts(self, p):

        if isinstance(p, Replace):
            self.parent.append(Replace)
            left, mid, right = p.str, p.old, p.new
            l_type, m_type, r_type = check_type(left), check_type(mid), \
                check_type(right)
            self.child.append([l_type, m_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, Concat):
            self.parent.append(Concat)
            left, right = p.x, p.y
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Substr):
            self.parent.append(Substr)
            left, mid, right = p.str, p.start, p.end
            l_type, m_type, r_type = check_type(left), check_type(mid), \
                check_type(right)
            self.child.append([l_type, m_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, IteStr):
            self.parent.append(IteStr)
            left, mid, right = p.condition, p.true_case, p.false_case
            l_type, m_type, r_type = check_type(left), check_type(mid), \
                check_type(right)
            self.child.append([l_type, m_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, Int2Str):
            self.parent.append(Int2Str)
            left = p.int
            l_type = check_type(left)
            self.child.append([l_type])
            self.size += 1
            self.get_parts(left)

        elif isinstance(p, At):
            self.parent.append(At)
            left, right = p.str, p.pos
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Equal):
            self.parent.append(Equal)
            left, right = p.int_left, p.int_right
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Contain):
            self.parent.append(Contain)
            left, right = p.str, p.item
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Suffixof):
            self.parent.append(Suffixof)
            left, right = p.str, p.item
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Prefixof):
            self.parent.append(Prefixof)
            left, right = p.str, p.item
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Str2Int):
            self.parent.append(Str2Int)
            left = p.str
            l_type = check_type(left)
            self.child.append([l_type])
            self.size += 1
            self.get_parts(left)

        elif isinstance(p, Equal):
            self.parent.append(Equal)
            left, right = p.left, p.right
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Plus):
            self.parent.append(Plus)
            left, right = p.left, p.right
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Minus):
            self.parent.append(Minus)
            left, right = p.left, p.right
            l_type, r_type = check_type(left), check_type(right)
            self.child.append([l_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Length):
            self.parent.append(Length)
            left = p.str
            l_type = check_type(left)
            self.child.append([l_type])
            self.size += 1
            self.get_parts(left)

        elif isinstance(p, IteInt):
            self.parent.append(IteInt)
            left, mid, right = p.condition, p.true_case, p.false_case
            l_type, m_type, r_type = check_type(left), check_type(mid), \
                check_type(right)
            self.child.append([l_type, m_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, IndexOf):
            self.parent.append(IndexOf)
            left, mid, right = p.input_str, p.item, p.start
            l_type, m_type, r_type = check_type(left), check_type(mid), \
                check_type(right)
            self.child.append([l_type, m_type, r_type])
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, Str):
            self.parent.append(p)
            self.child.append([p])
            self.size += 1

        elif isinstance(p, StrVar):
            self.parent.append(p)
            self.child.append([p])
            self.size += 1

        elif isinstance(p, Bool):
            self.parent.append(p)
            self.child.append([p])
            self.size += 1

        elif isinstance(p, Int):
            self.parent.append(p)
            self.child.append([p])
            self.size += 1

        elif isinstance(p, IntVar):
            self.parent.append(p)
            self.child.append([p])
            self.size += 1

    def remove_dup(self):
        zip_list = list(zip(self.parent, self.child))
        temp_list = []
        for i in zip_list:
            append = True
            for j in temp_list:
                a = j[0] == i[0]
                b = j[1] == i[1]
                if a==True and b==True:
                    append = False
                    break
            if append:
                temp_list.append(i)

        self.parent = []
        self.child = []
        for i in temp_list:
            self.parent.append(i[0])
            self.child.append(i[1])


class GetInsideProbe():
    def __init__(self):
        self.parent = []
        self.size = 0

    def get_parts(self, p):

        if isinstance(p, Replace):
            if Replace not in self.parent:
                self.parent.append(Replace)
            left, mid, right = p.str, p.old, p.new
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, Concat):
            if Concat not in self.parent:
                self.parent.append(Concat)
            left, right = p.x, p.y
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Substr):
            if Substr not in self.parent:
                self.parent.append(Substr)
            left, mid, right = p.str, p.start, p.end
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, IteStr):
            if IteStr not in self.parent:
                self.parent.append(IteStr)
            left, mid, right = p.condition, p.true_case, p.false_case
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, Int2Str):
            if Int2Str not in self.parent:
                self.parent.append(Int2Str)
            left = p.int
            self.size += 1
            self.get_parts(left)

        elif isinstance(p, At):
            if At not in self.parent:
                self.parent.append(At)
            left, right = p.str, p.pos
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Equal):
            if Equal not in self.parent:
                self.parent.append(Equal)
            left, right = p.int_left, p.int_right
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Contain):
            if Contain not in self.parent:
                self.parent.append(Contain)
            left, right = p.str, p.item
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Suffixof):
            if Suffixof not in self.parent:
                self.parent.append(Suffixof)
            left, right = p.str, p.item
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Prefixof):
            if Prefixof not in self.parent:
                self.parent.append(Prefixof)
            left, right = p.str, p.item
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Str2Int):
            if Str2Int not in self.parent:
                self.parent.append(Str2Int)
            left = p.str
            self.size += 1
            self.get_parts(left)

        elif isinstance(p, Equal):
            if Equal not in self.parent:
                self.parent.append(Equal)
            left, right = p.left, p.right
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Plus):
            if Plus not in self.parent:
                self.parent.append(Plus)
            left, right = p.left, p.right
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Minus):
            if Minus not in self.parent:
                self.parent.append(Minus)
            left, right = p.left, p.right
            self.size += 1
            self.get_parts(left)
            self.get_parts(right)

        elif isinstance(p, Length):
            if Length not in self.parent:
                self.parent.append(Length)
            left = p.str
            self.size += 1
            self.get_parts(left)

        elif isinstance(p, IteInt):
            if IteInt not in self.parent:
                self.parent.append(IteInt)
            left, mid, right = p.condition, p.true_case, p.false_case
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, IndexOf):
            if IndexOf not in self.parent:
                self.parent.append(IndexOf)
            left, mid, right = p.input_str, p.item, p.start
            self.size += 1
            self.get_parts(left)
            self.get_parts(mid)
            self.get_parts(right)

        elif isinstance(p, Str):
            if p not in self.parent:
                self.parent.append(p)
            self.size += 1

        elif isinstance(p, StrVar):
            if p not in self.parent:
                self.parent.append(p)
            self.size += 1

        elif isinstance(p, Bool):
            if p not in self.parent:
                self.parent.append(p)
            self.size += 1

        elif isinstance(p, Int):
            if p not in self.parent:
                self.parent.append(p)
            self.size += 1

        elif isinstance(p, IntVar):
            if p not in self.parent:
                self.parent.append(p)
            self.size += 1

# file_sexp = parser.sexpFromFile("2171308.sl")
# benchmark_tuple = parser.extract_benchmark(file_sexp)
# (
#     theories,
#     syn_ctx,
#     synth_instantiator,
#     macro_instantiator,
#     uf_instantiator,
#     constraints,
#     grammar_map,
#     forall_vars_map,
#     default_grammar_sfs
# ) = benchmark_tuple

# sample = f'(str.replace _arg_0 (str.substr _arg_0 1 (str.indexof _arg_0 " " 1)) " ")'
# left_b, right_b = list(find_all(sample, '(')), list(find_all(sample, ')'))
# l = len(left_b)

# previous = None
# p = None

# for i in range(l):
#     par_str = sample[left_b[l-i-1]+1: right_b[i]]
#     print(par_str)
#     if previous != None:
#         full = "(%s)" %previous
#         idx = par_str.index(full)
#         removed_str = par_str.replace(full, "OBJECT")
#         print(par_str)

#     parts = removed_str.split(" ")
#     if "indexof" in removed_str:
#         if p != None:
#             obj_loc = parts.index("OBJECT")
#             p = IndexOf(Str(parts[1]), Str(parts[2]), Int(parts[3]))
#     previous = par_str
#     print(previous)

    # specification, _ = make_specification(synth_funs, theory, syn_ctx, constraints)
    # program = Length(Replace(Str('a < 4 and a > 0'), Str('<'), Str('')))
    # p = At(Substr(Str('abcde'), Int(2), Int(4)), Int(0))
    # p = Bool(True)
    # p = Equal(Int(2),  Int(2))
    # p = Contain(Str('abcde'),  Int('z'))
    # p = Suffixof(Str('abcde'),  Int('d'))
    # p = Prefixof(Str('abcde'),  Int('a'))
    # p = IteInt(Equal(Int(2),  Int(3)), Plus(Int(2),  Int(2)), Minus(Int(2),  Int(2)))
    # p = IteStr(Equal(Int(2),  Int(2)), At(Substr(Str('abcde'), Int(2), Int(4)), Int(0)), Substr(Str('abcde'), Int(2), Int(4)))
    # print(p.toString())
    # print(p.interpret(None))
