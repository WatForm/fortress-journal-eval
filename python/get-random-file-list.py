import random
import os

dir_prefix = "../"
benchmark_dir = dir_prefix + "TPTP-v7.5.0/Problems/"
num_files = 3000

file_list = []
for (dirpath, dirnames, filenames) in os.walk(benchmark_dir):
    file_list.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.p') and '+' in f])
random.shuffle(file_list)
file_list = file_list[:num_files]

f = open("./random-file_list.txt", "w")
for i in file_list:
    f.write(i[len(benchmark_dir):] + '\n')
f.close()
