# This repository is for project of CMPUT 659 in University of Alberta.
# The owners are Guanfang Dong and Jiaqi He.
# For CMPUT 659 students, you should not copy any of code from our work.
import time
import numpy as np
from DSL_Str import *
from read_sl import ReadSL
import math
from itertools import combinations, chain
from timeout import timeout


class BUS():
    def __init__(self, max_time, bound, str_, int_, str_var, int_var, io_list):
        self.max_time = max_time
        self.bound = bound
        self.str_ = [Str(i) for i in str_]
        self.int_ = [Int(i) for i in int_]
        self.str_var = [StrVar(i) for i in str_var]
        self.int_var = [IntVar(i) for i in int_var]
        self.bool = [Bool(True), Bool(False)]
        self.io_list = io_list
        self.bank = self.str_ + self.int_ + self.bool + self.str_var + self.int_var
        self.phog_probe = init_phog_probe(self.str_, self.str_var,
                                          self.int_, self.bool)
        self.phog_probe_copy = self.phog_probe.copy()
        self.bank_type = []
        self.bank_state_type = []
        self.num_eval = 0
        self.bank_cost = self.init_bank_cost()
        self.all_result = set()
        self.start_time = time.time()

    def init_bank_cost(self):
        bank_cost = []
        for i in self.bank:
            if isinstance(i, Str):
                p = self.phog_probe[i][(i)]
                c = int(-math.log(p, 2))
                self.bank_type.append("Str")
                self.bank_state_type.append("S")
                bank_cost.append(c)
            elif isinstance(i, Int):
                p = self.phog_probe[i][(i)]
                c = int(-math.log(p, 2))
                self.bank_type.append("Int")
                self.bank_state_type.append("I")
                bank_cost.append(c)
            elif isinstance(i, Bool):
                p = self.phog_probe[i][(i)]
                c = int(-math.log(p, 2))
                self.bank_type.append("Bool")
                self.bank_state_type.append("B")
                bank_cost.append(c)
            elif isinstance(i, StrVar):
                p = self.phog_probe[i][(i)]
                self.bank_type.append("StrVar")
                self.bank_state_type.append("S")
                c = int(-math.log(p, 2))
                bank_cost.append(c)
        return bank_cost

    def gen_p_one_arg(self, p, type):
        """
        Generating programs with one input.
        input: DSL program, progrma_type
        output: list with all programs under this case
        """
        new_progs = []
        if type is "S":
            for dsl in [Str2Int, Length]:
                new_progs.append(dsl(p))
        elif type is "I":
            new_progs.append(Int2Str(p))
        return new_progs

    def gen_p_two_args(self, left, right, l_type, r_type):
        """
        Generating programs with two inputs.
        input: DSL program, progrma_type
        output: list with all programs under this case
        """
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
        """
        Generating programs with three inputs.
        input: DSL program, progrma_type
        output: list with all programs under this case
        """
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
        return new_progs

    def append_helper(self, old_list, new_list):
        """
        heler to append list to another list
        """
        if new_list is not None:
            for i in new_list:
                old_list.append(i)

    def subset_collection(self, input_output):
        pairs_length = len(input_output)
        subsets = list(chain(*[combinations(range(pairs_length), ni)
                               for ni in range(pairs_length+1)]))[1:]

        return subsets

    def normalize_phog_prob(self):
        fir_keys = self.phog_probe.keys()
        sum_possi = 0
        for i in fir_keys:
            sec_keys = self.phog_probe[i].keys()
            for j in sec_keys:
                possi = self.phog_probe[i][j]
                sum_possi += possi
        for i in fir_keys:
            sec_keys = self.phog_probe[i].keys()
            for j in sec_keys:
                self.phog_probe[i][j] = self.phog_probe[i][j]/sum_possi

    def restart(self):
        self.bank = self.str_ + self.int_ + self.bool + self.str_var + self.int_var
        self.bank_type = []
        self.bank_state_type = []
        self.bank_cost = self.init_bank_cost()
        self.all_result = set()

    def grow(self, prev_cost):
        """
        This function allows to grow new functions under currrent bank
        """
        new_progs = []

        all_types = np.array(self.bank_type)
        np_bank_costs = np.array(self.bank_cost)
        np_bank = np.array(self.bank)

        p_names = get_str_names()
        cost_dict = {}
        same_type_dict = {}

        for i in p_names:
            possi_cost_idx = np.where(all_types == i)
            same_type_dict[i] = possi_cost_idx
            possi_cost = np_bank_costs[possi_cost_idx]
            possi_cost = np.unique(possi_cost)
            cost_dict[i] = possi_cost

        all_possi_cost = []
        all_possi_candi = []
        all_possi_tcombo = []
        all_possi_init_p = []

        all_keys = get_keys()

        for key in all_keys:
            s_dict = self.phog_probe[key]
            contexts = s_dict.keys()
            if key == contexts:
                continue
            for each_c in contexts:
                try:
                    c_length = len(each_c)
                except:
                    c_length = 1
                if c_length is 3:
                    t_1, t_2, t_3 = get_node_str(each_c[0]), \
                        get_node_str(each_c[1]), get_node_str(each_c[2])

                    p_cost_t1, p_cost_t2, p_cost_t3 = cost_dict[t_1], \
                        cost_dict[t_2], cost_dict[t_3]

                    for p_cost_1 in p_cost_t1:
                        for p_cost_2 in p_cost_t2:
                            for p_cost_3 in p_cost_t3:
                                p_cost = p_cost_1 + p_cost_2 + p_cost_3
                                context_p = self.phog_probe[key][each_c]
                                p_cost += int(-math.log(context_p, 2))

                                all_possi_cost.append(p_cost)
                                all_possi_candi.append([p_cost_1, p_cost_2,
                                                        p_cost_3])
                                all_possi_tcombo.append([t_1, t_2, t_3])
                                all_possi_init_p.append([key, each_c])

                if c_length is 2:
                    t_1, t_2 = get_node_str(each_c[0]), get_node_str(each_c[1])

                    p_cost_t1, p_cost_t2 = cost_dict[t_1], cost_dict[t_2]
                    for p_cost_1 in p_cost_t1:
                        for p_cost_2 in p_cost_t2:
                            p_cost = p_cost_1 + p_cost_2
                            context_p = self.phog_probe[key][each_c]
                            p_cost += int(-math.log(context_p, 2))

                            all_possi_cost.append(p_cost)
                            all_possi_candi.append([p_cost_1, p_cost_2])
                            all_possi_tcombo.append([t_1, t_2])
                            all_possi_init_p.append([key, each_c])

                if c_length is 1:
                    t_1 = get_node_str(each_c)
                    p_cost_t1 = cost_dict[t_1]
                    for p_cost_1 in p_cost_t1:
                        p_cost = p_cost_1
                        context_p = self.phog_probe[key][each_c]
                        p_cost += int(-math.log(context_p, 2))

                        all_possi_cost.append(p_cost)
                        all_possi_candi.append([p_cost_1])
                        all_possi_tcombo.append([t_1])
                        all_possi_init_p.append([key, [each_c]])

        all_possi_cost = np.array(all_possi_cost)
        all_possi_candi = np.array(all_possi_candi)
        all_possi_tcombo = np.array(all_possi_tcombo)
        all_possi_init_p = np.array(all_possi_init_p)

        all_possi_cost = all_possi_cost.astype('int')

        idx = np.where(all_possi_cost > prev_cost)

        all_possi_cost = all_possi_cost[idx]

        all_possi_candi = all_possi_candi[idx]
        all_possi_tcombo = all_possi_tcombo[idx]
        all_possi_init_p = all_possi_init_p[idx]

        min_cost = np.amin(all_possi_cost)
        cost_idx = np.argwhere(all_possi_cost == min_cost)

        all_possi_cost = all_possi_cost[cost_idx]
        all_possi_candi = all_possi_candi[cost_idx]
        all_possi_tcombo = all_possi_tcombo[cost_idx]
        all_possi_init_p = all_possi_init_p[cost_idx]


        for i in range(len(all_possi_cost)):
            base_p = all_possi_init_p[i][0][0]
            inner_p_list = all_possi_init_p[i][0][1]

            p_idx_save = []

            for step, j in enumerate(inner_p_list):
                str_name = get_node_str(j)
                type_idx = same_type_dict[str_name]
                type_cost = all_possi_candi[i][0][step]
                all_cost_idx = np.argwhere(np_bank_costs == type_cost)

                all_s_idx = np.intersect1d(all_cost_idx, type_idx)
                p_idx_save.append(all_s_idx)

            p_len = len(p_idx_save)
            if p_len == 3:
                idx_1, idx_2, idx_3 = p_idx_save[0], p_idx_save[1], p_idx_save[2]
                p_1, p_2, p_3 = np_bank[idx_1], np_bank[idx_2], np_bank[idx_3]
                for j in p_1:
                    for k in p_2:
                        for q in p_3:
                            new_p = base_p(j, k, q)
                            new_progs.append(new_p)
            elif p_len == 2:
                idx_1, idx_2 = p_idx_save[0], p_idx_save[1]
                p_1, p_2 = np_bank[idx_1], np_bank[idx_2]
                for j in p_1:
                    for k in p_2:
                        new_p = base_p(j, k)
                        new_progs.append(new_p)
            elif p_len == 1:
                idx_1 = p_idx_save[0]
                p_1 = np_bank[idx_1]
                for j in p_1:
                    new_p = base_p(j)
                    new_progs.append(new_p)
        return new_progs, min_cost

    def synthesize(self, debug, weak_detect):
        prev_cost = 0
        idx_subsets = self.subset_collection(self.io_list)
        print(idx_subsets)

        cont = True

        for level in range(self.bound):
            print("current level is %d" % level)
            new_progs, prev_cost = self.grow(prev_cost)
            cont = True
            for p in new_progs:
                if time.time() - self.start_time > self.max_time:
                    raise Exception
                if cont == False:
                    break
                try:
                    io_len = len(self.io_list)
                    match_idx = []
                    one_result = ""
                    for step, io in enumerate(self.io_list):
                        result = p.interpret(io)
                        one_result += str(result)
                        if result == io["out"]:
                            match_idx.append(step)
                            io_len -= 1
                    self.num_eval += 1
                except:
                    pass

                if tuple(match_idx) == idx_subsets[-1]:
                    solution = p.toString()
                    current_time = time.time()
                    time_usage = current_time - self.start_time
                    g = GetInsideProbe()
                    g.get_parts(p)
                    parent = g.parent
                    solution_size = g.size
                    current_distri = self.phog_probe
                    init_distri = self.phog_probe_copy
                    return solution, self.num_eval, time_usage, \
                            solution_size, current_distri, init_distri
                
                if tuple(match_idx) in idx_subsets:
                    print(tuple(match_idx))
                    g = GetInside()
                    g.get_parts(p)
                    g.remove_dup()
                    parent, child = g.parent, g.child
                    perc_solve = len(match_idx) / len(self.io_list)
                    for step, i in enumerate(parent):
                        if len(child[step]) > 1:
                            new_prob = self.phog_probe[i][tuple(child[step])]
                        elif len(child[step]) == 1:
                            new_prob = self.phog_probe[i][child[step][0]]

                        new_prob = new_prob ** (1-perc_solve)

                        if len(child[step]) > 1:
                            self.phog_probe[i][tuple(child[step])] = new_prob
                        elif len(child[step]) == 1:
                            self.phog_probe[i][child[step][0]] = new_prob

                        
                        print(parent[step])
                        print(child[step])
                        print(new_prob)
                        print("\n")

                    self.normalize_phog_prob()
                    print("partial solution or solution found:",
                          p.toString())
                    idx_subsets.remove(tuple(match_idx))
                    self.restart()
                    cont = False
                    prev_cost = 0

                if not weak_detect:
                    self.bank.append(p)
                    self.bank_type.append(get_type_str(p))
                    self.bank_cost.append(prev_cost)
                else:
                    if one_result not in self.all_result:
                        self.bank.append(p)
                        self.bank_type.append(get_type_str(p))
                        self.bank_cost.append(prev_cost)
                        self.all_result.add(one_result)

            print("current bank length", len(self.bank))
            print(prev_cost)


def phog_probe_solver(file_path):
    f = ReadSL(file_path)
    str_var, str_, int_var, int_, input, output = f.get_attrs()

    bound = 10000
    max_time = 300
    io_list = []

    for step, i in enumerate(input):
        io_pairs = {}
        for arg_index, arg in enumerate(str_var):
            io_pairs[arg] = i
        io_pairs["out"] = output[step]
        io_list.append(io_pairs)

    solver = BUS(max_time, bound, str_, int_, str_var, int_var, io_list)
    solution, num_eval, time_usage, solution_size, current_distri, init_distri = \
        solver.synthesize(debug=True, weak_detect=True)
    print("num_eval:", num_eval)
    print("solution:", solution)
    print("time_usage", time_usage)
    print("solution_size", solution_size)
    return solution, num_eval, time_usage, solution_size, current_distri, init_distri
