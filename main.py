import os
import time
from tqdm import tqdm
import gc

from memory_profiler import profile

import core_functions.bm25 as bm25
import core_functions.clustering.cluster_data as cl_cl
import core_functions.handle_data as hd
import core_functions.index_data as idxd
import core_functions.pickle_usage as pck
import core_functions.tf_idf as ti
from core_functions import Const
import core_functions.bloc_working as bw
from multiprocessing import Process, Pipe


def main_bloc_creation(nb_total_docs):
    # *------------------------------------------*
    print("Creating indexes...", bw.memory_usage(), "Mo")
    nb_docs_done = 0
    bloc_num = 0
    while nb_docs_done < nb_total_docs:
        print("\n", nb_docs_done, "/", nb_total_docs, "done...", bw.memory_usage(), "Mo")

        parent_conn, child_conn = Pipe()
        p = Process(target=bw.bloc_indexing,
                    args=(nb_docs_done, bloc_num, nb_total_docs, child_conn))
        p.start()
        nb_docs_done = parent_conn.recv()
        p.join()

        bloc_num += 1

    # *------------------------------------------*
    print("Splitting indexes...", bw.memory_usage(), "Mo")
    start_end_groups = pck.pickle_load("start_end_groups", "")
    # total_bloc_nb = 2
    # # total_bloc_nb = bloc_num + 1
    # # for bloc_num in range(total_bloc_nb):
    bloc_num = 0
    while os.path.isdir("data/pickle_files/b_{}".format(bloc_num)):
        p = Process(target=bw.split_indexes,
                    args=(bloc_num, start_end_groups))
        p.start()
        p.join()

        bloc_num += 1

    # *------------------------------------------*
    print("Merging indexes...", bw.memory_usage(), "Mo")
    bloc_num = 1
    while os.path.isdir("data/pickle_files/b_{}".format(bloc_num)):
        p = Process(target=bw.bloc_merging,
                    args=(bloc_num,))
        p.start()
        p.join()

        bloc_num += 1

    # *------------------------------------------*
    print("Calculating tf * idf...", bw.memory_usage(), "Mo")
    sub_bloc_num = 0
    while os.path.isdir("data/pickle_files/b_{}/b_{}_{}".format(0,
                                                                0, sub_bloc_num)):
        p = Process(target=bw.calculate_tf_idf,
                    args=(sub_bloc_num,))
        p.start()
        p.join()

        sub_bloc_num += 1


def main_bloc_after_creation():
    start_end_groups = pck.pickle_load("start_end_groups", "")

    query_test = "israël jérusalem"
    query_test = "président hollande"

    docnum_score_sum_dict = \
        bm25.big_query_bm25(query_test, start_end_groups)

    path_name = "b_{}/num_name_dict_b{}".format(0, 0)
    num_name_dict = pck.pickle_load(path_name, "")

    for key, value in sorted(docnum_score_sum_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print("{}: \t{}".format(num_name_dict[key], value))


def main():
    main_bloc_creation(100000)
    # main_bloc_after_creation()
    # bloc_num = 0
    # sub_bloc_num = 2
    # path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(bloc_num,
    #                                                        bloc_num, sub_bloc_num,
    #                                                        bloc_num, sub_bloc_num)
    # word_num_dict = pck.pickle_load(path_name, "")
    # print(word_num_dict)
if __name__ == '__main__':
    t_start = time.time()

    main()

    t_end = time.time()

    print("Running time = {} second(s)\n".format(t_end - t_start))
