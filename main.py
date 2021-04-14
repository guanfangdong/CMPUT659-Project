from phog_probe import phog_probe_solver
from probe import probe_solver
import pickle
import time
import os

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    trained_data = current_path + "benchmarks/string/train/"
    test_data = current_path + "benchmarks/string/train/"

    result_path = current_path + "result/"


    train_names = os.listdir(trained_data)
    for i in train_names:
        full_path = trained_data + i
        start_time = time.time()
        try:

            phog_probe_result = phog_probe_solver(full_path)

            name = i.split(".")[0]
            f = open('%s%s_phog_probe.pckl' % (result_path, name), 'wb')
            pickle.dump(phog_probe_result, f)
            f.close()
            start_time = time.time()

        except:
            process = time.time() - start_time
            record_txt = open("record.txt", "a")
            record_txt.write("error on phog_probe\n")
            record_txt.write(full_path + "\n")
            record_txt.write(str(process) + "\n")
            record_txt.close()
            start_time = time.time()

        try:
            probe_result = probe_solver(full_path)

            name = i.split(".")[0]
            f = open('%s%s_probe.pckl' % (result_path, i), 'wb')
            pickle.dump(probe_result, f)
            f.close()

        except:
            process = time.time() - start_time
            record_txt = open("record.txt", "a")
            record_txt.write("error on probe\n")
            record_txt.write(full_path + "\n")
            record_txt.write(str(process) + "\n")
            record_txt.close()
