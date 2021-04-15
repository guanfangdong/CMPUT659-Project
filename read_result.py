import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from DSL_Str import *


def pad_to_dense(M):
    """Appends the minimal required amount of zeroes at the end of each 
     array in the jagged array `M`, such that `M` looses its jagedness."""

    maxlen = max(len(r) for r in M)

    Z = np.zeros((len(M), maxlen))
    for enu, row in enumerate(M):
        Z[enu, :len(row)] += row 
    return Z

def heatmap(title, table, x, y, x_label, y_label):
    fig, ax = plt.subplots()
    im = ax.imshow(table)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(y)):
    #     for j in range(len(x)):
    #         text = ax.text(j, i, table[i, j],
    #                     ha="center", va="center", color="w")

    ax.set_title(title)
    fig.tight_layout()
    plt.show()





def scatter(title, x_a, x_b, a, b, a_legend, b_legend, x_label, y_label):
    # style
    plt.style.use('seaborn-darkgrid')

    

    legend1 = plt.scatter(x_a, a, c='b', s=20, label=a_legend,
               alpha=1, edgecolors='none')
    
    legend2 = plt.scatter(x_b, b, c='g', s=20, label=b_legend,
               alpha=1, edgecolors='none')

    plt.legend([legend1, legend2], [a_legend, b_legend])

    plt.title(title, loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(title)
    plt.close()




def gen_plot(title, x, a, b, a_legend, b_legend, x_label, y_label):


    # Make a data frame
    df=pd.DataFrame({'x': x, a_legend: a, b_legend: b})

    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num=0
    for column in df.drop('x', axis=1):
        num+=1
        plt.plot(df['x'], df[column], marker='o', color=palette(num), linewidth=1, alpha=0.9, label=column)

    # Add legend
    plt.legend(loc=2, ncol=2)

    # Add titles
    plt.title(title, loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig(title)
    plt.close()


def gen_plot_one(title, x, a, x_label, y_label, y_legned, right = False, y_lim = False):


    # Make a data frame
    df=pd.DataFrame({'x': x, y_legned: a})

    # style
    plt.style.use('seaborn-darkgrid')

    if y_lim:
        plt.ylim(-1, 1)

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot

    num=0
    for column in df.drop('x', axis=1):
        num+=1
        plt.xticks(rotation=45)
        plt.plot(df['x'], df[column], marker='o', color=palette(num), linewidth=1, alpha=0.9, label=column)

    # Add legend
    plt.legend(loc=2, ncol=2)
    if right:
        plt.xticks(rotation=45)

    # Add titles
    plt.title(title, loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig(title)
    plt.close()

def get_ave_table(dict_list):
    dict_len = len(dict_list[0])
    dict_keys_1 = dict_list[0].keys()
    all_nont_keys = []
    x = []
    table = []
    
    for i in dict_keys_1:
        key_str = get_node_str(i)
        if key_str != None:
            x.append(key_str)
            all_nont_keys.append(i)

    for step, each_dict in enumerate(dict_list):
        record = []
        for i in all_nont_keys:
            second_dict = each_dict[i]
            second_dict_list = list(second_dict.values())
            record.append(second_dict_list)
        table.append(record)

    new_table = []
    for record in table:
        new_table.append(pad_to_dense(record))
    new_table = np.array(new_table)
    ave_table = np.average(new_table, axis=0)

    return ave_table, x

if __name__ == "__main__":

    phog_probe_succeed = 0
    phog_probe_fail = 0

    probe_succeed = 0
    probe_fail = 0

    phog_probe_eval = []
    probe_eval = []

    phog_probe_time = []
    probe_time = []

    phog_probe_size = []
    probe_size = []

    phog_probe_dist_ori = []
    phog_probe_dist_changed = []

    probe_dist_ori = []
    probe_dist_changed = []

    pass_both_eval = []


    current_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    trained_data = current_path + "benchmarks/string/train/"
    result_path = current_path + "result/"

    all_trained_data = os.listdir(trained_data)

    fail_txt = open("record.txt", "r")
    fail_lines = fail_txt.readlines()
    fail_txt.close()
    

    for i in all_trained_data:

        pass_phog_probe = False
        pass_probe = False

        name = i.split('.')[0]
        phog_probe_name = name + "_phog_probe.pckl"
        probe_name = name + ".sl_probe.pckl"
        try:
            f = open('%s%s' % (result_path, phog_probe_name), 'rb')
            obj = pickle.load(f)
            (solution, num_eval_1, time_usage_1, solution_size_1,
             current_distri_1, init_distri_1) = obj
            f.close()

            phog_probe_succeed += 1
            phog_probe_eval.append(num_eval_1)
            phog_probe_time.append(int(time_usage_1))
            phog_probe_size.append(solution_size_1)
            phog_probe_dist_ori.append(init_distri_1)
            phog_probe_dist_changed.append(current_distri_1)

            pass_phog_probe = True

        except:
            for step, line in enumerate(fail_lines):
                if name in line:
                    if "phog_probe" in fail_lines[step-1]:
                        time_usage = float(fail_lines[step+1].strip("\n"))
                        if time_usage > 50:
                            phog_probe_fail += 1

        try:
            f = open('%s%s' % (result_path, probe_name), 'rb')
            obj = pickle.load(f)
            (solution, num_eval_2, time_usage_2, solution_size_2,
             current_distri_2, init_distri_2) = obj
            f.close()

            probe_succeed += 1
            probe_eval.append(num_eval_2)
            probe_time.append(int(time_usage_2))
            probe_size.append(solution_size_2)
            probe_dist_ori.append(init_distri_2)
            probe_dist_changed.append(current_distri_2)

            pass_probe = True

        except:
            for step, line in enumerate(fail_lines):
                if name in line:
                    if "error on probe" in fail_lines[step-1]:
                        time_usage = float(fail_lines[step+1].strip("\n"))
                        if time_usage > 50:
                            probe_fail += 1

        if pass_probe and pass_phog_probe:
            pass_both_eval.append([num_eval_1, num_eval_2])

    diff_prop_list = []
    for i in pass_both_eval:
        diff = i[1] - i[0]
        diff_prop = diff / max(i)
        diff_prop_list.append(diff_prop)

    # fig 1
    title = "Evaluation Programs Difference by Proportionality"
    x = range(len(diff_prop_list))
    y = diff_prop_list
    x_label = "Program index"
    y_label = "Proportion"
    y_legned = ">0: probe more than phog_probe <0: phog_probe more than probe"
    gen_plot_one(title, x, y, x_label, y_label, y_legned, y_lim=True)

    time_interval = [60, 120, 180, 240, 300]
    phog_probe_interval_count = []
    probe_interval_count = []
    # fig 2
    phog_probe_time_back = phog_probe_time[:]
    probe_time_back = probe_time[:]
    for step, i in enumerate([phog_probe_time, probe_time]):
        for j in time_interval:
            count = 0
            for k in i:
                if k<=j:
                    count+=1
                    i.remove(k)
            if step == 0:
                phog_probe_interval_count.append(count)
            elif step == 1:
                probe_interval_count.append(count)

    phog_probe_interval_count.append(phog_probe_fail)
    probe_interval_count.append(probe_fail)

    title = "Time vs Program Solved"
    x = ["<1min", "1min-2min", "2min-3min", "3min-4min",
                 "4min-5min", ">5min"]
    a = phog_probe_interval_count
    b = probe_interval_count
    a_legend = "phog_probe"
    b_legend = "probe"
    x_label = "Time interval"
    y_label = "Number of programs"
    gen_plot(title, x, a, b, a_legend, b_legend, x_label, y_label)

    #  fig 3
    title = "Size vs Time Usage"
    x_a = phog_probe_time_back
    x_b = probe_time_back
    a = phog_probe_size
    b = probe_size
    a_legend = "phog_probe"
    b_legend = "probe"
    x_label = "Time usage"
    y_label = "Program size"
    scatter(title, x_a, x_b, a, b, a_legend, b_legend, x_label, y_label)

    # fig 4
    title = "Size vs Program Eval"
    x_a = phog_probe_eval
    x_b = probe_eval
    a = phog_probe_size
    b = probe_size
    a_legend = "phog_probe"
    b_legend = "probe"
    x_label = "Program eval"
    y_label = "Program size"
    scatter(title, x_a, x_b, a, b, a_legend, b_legend, x_label, y_label)

    # fig 5
    phog_ori = init_phog_probe([],[],[],[])
    a = []
    for i in phog_ori.values():
        a.append(list(i.values()))
    

    phog_ori = pad_to_dense(a)
    phog_changed, x = get_ave_table(phog_probe_dist_changed)
    table  = phog_changed - phog_ori
    y = list(range(phog_changed.shape[1]))
    x_label = "Object"
    y_label = "Distribution Changed"
    y_legned = "phog_probe"
    table = np.sum(table,axis=1)
    
    title = "phog_probe Average Sum of Distribution Changed"
    gen_plot_one(title, x, table, x_label, y_label, y_legned, right=True)

    # fig 6
    

    probe_after = []
    for i in probe_dist_changed:
        v = list(i.values())
        length = len(v)
        probe_ori = [1/length] * length
        v, probe_ori = np.array(v), np.array(probe_ori)
        change = v - probe_ori
        probe_after.append(change[:16])

    probe_after = np.array(probe_after)
    probe_after = np.average(probe_after, axis=0)

    title = "probe Average Distribution Changed"
    y_legned = "probe"

    gen_plot_one(title, x, probe_after, x_label, y_label, y_legned, right=True)
    
    