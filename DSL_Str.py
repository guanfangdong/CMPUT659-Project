import copy
from parsers import parser
import re


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


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
        return "%s.IndexOf(%s, %s)" (self.input_str.toString(), self.item.toString(), self.start.toString())

    def interpret(self, env):
        return self.input_str.interpret(env)[self.start.interpret(env):].index(self.item.interpret(env))


file_sexp = parser.sexpFromFile("2171308.sl")
benchmark_tuple = parser.extract_benchmark(file_sexp)
(
    theories,
    syn_ctx,
    synth_instantiator,
    macro_instantiator,
    uf_instantiator,
    constraints,
    grammar_map,
    forall_vars_map,
    default_grammar_sfs
) = benchmark_tuple

sample = f'(str.replace _arg_0 (str.substr _arg_0 1 (str.indexof _arg_0 " " 1)) " ")'
left_b, right_b = list(find_all(sample, '(')), list(find_all(sample, ')'))
l = len(left_b)

previous = None
p = None

for i in range(l):
    par_str = sample[left_b[l-i-1]+1: right_b[i]]
    print(par_str)
    if previous != None:
        full = "(%s)" %previous
        idx = par_str.index(full)
        removed_str = par_str.replace(full, "OBJECT")
        print(par_str)

    parts = removed_str.split(" ")
    if "indexof" in removed_str:
        if p != None:
            obj_loc = parts.index("OBJECT")
            p = IndexOf(Str(parts[1]), Str(parts[2]), Int(parts[3]))
    previous = par_str
    print(previous)


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
