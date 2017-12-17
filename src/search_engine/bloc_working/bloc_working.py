import src.search_engine.bm25 as bm25
import src.search_engine.pickle_usage as pck
import src.search_engine.index_data as id
import src.search_engine.bloc_working.bloc_splitting as bs
import src.search_engine.bloc_working.bloc_merging as bm
import src.search_engine.tf_idf as ti
import src.other.memory_usage as mem

import os
from multiprocessing import Process, Pipe


def indexes_creation(nb_total_docs):
    # *------------------------------------------*
    print("Creating indexes...", mem.memory_usage(), "Mo")
    nb_docs_done = 0
    bloc_num = 0
    while nb_docs_done < nb_total_docs:
        print("\n", nb_docs_done, "/", nb_total_docs, "done...", mem.memory_usage(), "Mo")

        parent_conn, child_conn = Pipe()
        p = Process(target=id.bloc_indexing,
                    args=(nb_docs_done, bloc_num, nb_total_docs, child_conn))
        p.start()
        nb_docs_done = parent_conn.recv()
        p.join()

        bloc_num += 1

    # *------------------------------------------*
    print("Splitting indexes...", mem.memory_usage(), "Mo")
    start_end_groups = pck.pickle_load("start_end_groups", "")
    # total_bloc_nb = 2
    # # total_bloc_nb = bloc_num + 1
    # # for bloc_num in range(total_bloc_nb):
    bloc_num = 0
    while os.path.isdir("data/pickle_files/b_{}".format(bloc_num)):
        p = Process(target=bs.split_indexes,
                    args=(bloc_num, start_end_groups))
        p.start()
        p.join()

        bloc_num += 1

    # *------------------------------------------*
    print("Merging indexes...", mem.memory_usage(), "Mo")
    bloc_num = 1
    while os.path.isdir("data/pickle_files/b_{}".format(bloc_num)):
        p = Process(target=bm.bloc_merging,
                    args=(bloc_num,))
        p.start()
        p.join()

        bloc_num += 1

    # *------------------------------------------*
    print("Calculating tf * idf...", mem.memory_usage(), "Mo")
    sub_bloc_num = 0
    while os.path.isdir("data/pickle_files/b_{}/b_{}_{}".format(0,
                                                                0, sub_bloc_num)):
        p = Process(target=ti.calculate_tf_idf,
                    args=(sub_bloc_num,))
        p.start()
        p.join()

        sub_bloc_num += 1


def query(query=None):
    start_end_groups = pck.pickle_load("start_end_groups", "")
    if query is None:
        query = "israël jérusalem"
        query = "président hollande"

    docnum_score_sum_dict = \
        bm25.bm25(query, start_end_groups)

    path_name = "b_{}/num_name_dict_b{}".format(0, 0)
    num_name_dict = pck.pickle_load(path_name, "")

    for key, value in sorted(docnum_score_sum_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print("{}: \t{}".format(num_name_dict[key], value))


if __name__ == '__main__':
    pass
