import pickle
import os


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    result_path = current_path + "result/"
    name = "11440431_phog_probe"
    f = open('%s%s.pckl' %(result_path, name), 'rb')
    obj = pickle.load(f)
    (solution, num_eval, time_usage, solution_size, 
    current_distri, init_distri) = obj
    print(solution_size)
    f.close()