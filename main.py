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
    print("Creating indexes...")
    nb_docs = 0
    bloc_num = 0
    while nb_docs < nb_total_docs:
        print(nb_docs, " / ", nb_total_docs, " done...")

        parent_conn, child_conn = Pipe()
        p = Process(target=bw.bloc_indexing,
                    args=(nb_docs, bloc_num, nb_total_docs, child_conn))
        p.start()
        nb_docs = parent_conn.recv()
        p.join()

        bloc_num += 1

    # # *------------------------------------------*
    # # CAN BE IMPROVED if we need to reduce memory usage
    # print("Merging indexes...")
    # gap = 1
    # while gap < total_nb_blocs:
    #     gap *= 2
    #     # NEED MULTIPROCESSING
    #     for blocnum in range(0, total_nb_blocs, gap):
    #         neighboor_blocnum = int(blocnum + gap / 2)
    #         bw.bloc_merging(blocnum, neighboor_blocnum)
    #
    # # *------------------------------------------*
    # print("Splitting indexes...")
    # if total_nb_blocs_index > 1:
    #     bw.split_indexes(total_nb_blocs_index)
    #
    # # *------------------------------------------*
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
    main_bloc_creation(1200)
    # main_bloc_after_creation()


if __name__ == '__main__':
    t_start = time.time()

    main()

    t_end = time.time()

    print("Running time = {} second(s)\n".format(t_end - t_start))
