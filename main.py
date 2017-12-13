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
    total_bloc_nb = 2
    # total_bloc_nb = bloc_num + 1

    start_end_groups = pck.pickle_load("start_end_groups", "")

    for bloc_num in range(total_bloc_nb):
        p = Process(target=bw.split_indexes,
                    args=(bloc_num, start_end_groups))
        p.start()
        p.join()

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
    # TODO
    # print("Calculating tf * idf...")
    # for blocnum in range(0, total_nb_blocs_index, 1):
    #     bw.calculate_tf_idf(blocnum, total_nb_blocs_index)
    # # merging
    # gap = 1
    # while gap < total_nb_blocs_index:
    #     gap *= 2
    #     for blocnum in range(0, total_nb_blocs_index, gap):
    #         neighboor_blocnum = int(blocnum + gap / 2)
    #         bw.bloc_merging2(blocnum, neighboor_blocnum)


def main_bloc_after_creation():
    num_name_dict = pck.pickle_load("num_name_dict_b0", "")
    word_num_dict = pck.pickle_load("word_num_dict_b0", "")
    infos_doc_dict = pck.pickle_load("infos_doc_dict_b0", "")
    tf_idf_dict = pck.pickle_load("tf_idf_dict_b0", "")
    tf_dict = pck.pickle_load("tf_dict_b0", "")

    query_test = "israël jérusalem"
    # query_test = "président hollande"
    stopwords = hd.load_stopwords_set()

    bm25.test_dict(tf_idf_dict)

    # CAN BE IMPROVED if we need to reduce memory usage
    docnum_score_sum_dict = \
        bm25.bm25_function(query_test, stopwords, word_num_dict, tf_idf_dict, tf_dict, infos_doc_dict)

    for key, value in sorted(docnum_score_sum_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print("{}: \t{}".format(num_name_dict[key], value))


def main():
    main_bloc_creation(3200)
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
