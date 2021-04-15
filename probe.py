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
        self.probe = init_probe(self.str_, self.str_var, self.int_, self.bool)
        self.probe_copy = self.probe.copy()
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
                p = self.probe[i]
                c = int(-math.log(p, 2))
                self.bank_type.append("Str")
                self.bank_state_type.append("S")
                bank_cost.append(c)
            elif isinstance(i, Int):
                p = self.probe[i]
                c = int(-math.log(p, 2))
                self.bank_type.append("Int")
                self.bank_state_type.append("I")
                bank_cost.append(c)
            elif isinstance(i, Bool):
                p = self.probe[i]
                c = int(-math.log(p, 2))
                self.bank_type.append("Bool")
                self.bank_state_type.append("B")
                bank_cost.append(c)
            elif isinstance(i, StrVar):
                p = self.probe[i]
                self.bank_type.append("StrVar")
                self.bank_state_type.append("S")
                c = int(-math.log(p, 2))
                bank_cost.append(c)
        return bank_cost

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
        fir_keys = self.probe.keys()
        sum_possi = 0
        for i in fir_keys:
            possi = self.probe[i]
            sum_possi += possi
        for i in fir_keys:
            self.probe[i] = self.probe[i]/sum_possi

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

        all_types = np.array(self.bank_state_type)
        np_bank_costs = np.array(self.bank_cost)
        np_bank = np.array(self.bank)

        p_names = ["S", "B", "I"]
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

            key_cost = self.probe[key]
            key_cost = int(-math.log(key_cost, 2))

            child_types = get_content_types(key)
            types_len = len(child_types)

            if types_len == 3:
                avail_1, avail_2, avail_3 = cost_dict[child_types[0]], \
                        cost_dict[child_types[1]], cost_dict[child_types[2]]
                for cost_1 in avail_1:
                    for cost_2 in avail_2:
                        for cost_3 in avail_3:
                            total_cost = cost_1 + cost_2 + cost_3 + key_cost
                            candi = [cost_1, cost_2, cost_3]
                            tcombo = child_types
                            init_p = key
                            
                            all_possi_cost.append(total_cost)
                            all_possi_candi.append(candi)
                            all_possi_tcombo.append(tcombo)
                            all_possi_init_p.append(init_p)

            elif types_len == 2:
                avail_1, avail_2 = cost_dict[child_types[0]], \
                                cost_dict[child_types[1]]
                for cost_1 in avail_1:
                    for cost_2 in avail_2:
                        total_cost = cost_1 + cost_2 + key_cost
                        candi = [cost_1, cost_2]
                        tcombo = child_types
                        init_p = key
                            
                        all_possi_cost.append(total_cost)
                        all_possi_candi.append(candi)
                        all_possi_tcombo.append(tcombo)
                        all_possi_init_p.append(init_p)

            elif types_len == 1:
                avail_1 = cost_dict[child_types[0]]
                for cost_1 in avail_1:
                    total_cost = cost_1 + key_cost
                    candi = [cost_1]
                    tcombo = child_types
                    init_p = key
                        
                    all_possi_cost.append(total_cost)
                    all_possi_candi.append(candi)
                    all_possi_tcombo.append(tcombo)
                    all_possi_init_p.append(init_p)


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

            base_p = all_possi_init_p[i][0]
            child_type = all_possi_tcombo[i][0]
            child_cost = all_possi_candi[i][0]

            p_idx_save = []

            for step, j in enumerate(child_type):
                type_idx = same_type_dict[j]
                type_cost = child_cost[step]
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
            new_progs, prev_cost = self.grow(prev_cost)
            print("current level is %d" % level)
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
                    current_distri = self.probe
                    init_distri = self.probe_copy
                    return solution, self.num_eval, time_usage, \
                        solution_size, current_distri, init_distri

                if tuple(match_idx) in idx_subsets:

                    g = GetInsideProbe()
                    g.get_parts(p)
                    parent = g.parent
                    perc_solve = len(match_idx) / len(self.io_list)
                    for step, i in enumerate(parent):

                        new_prob = self.probe[i]
                        new_prob = new_prob ** (1-perc_solve)
                        self.probe[i] = new_prob

                        print(parent[step])
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
                    self.bank_state_type.append(get_type(p))
                    self.bank_cost.append(prev_cost)
                else:
                    if one_result not in self.all_result:
                        self.bank.append(p)
                        self.bank_type.append(get_type_str(p))
                        self.bank_state_type.append(get_type(p))
                        self.bank_cost.append(prev_cost)
                        self.all_result.add(one_result)
                if cont == False:
                    self.restart()

            print("current bank length", len(self.bank))
            print(prev_cost)



def probe_solver(file_path):
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
    print("solution:", solution)
    print("num_eval:", num_eval)
    print("time_usage", time_usage)
    print("solution_size", solution_size)
    return solution, num_eval, time_usage, solution_size, current_distri, init_distri
