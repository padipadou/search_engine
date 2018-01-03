import time
import argparse
from multiprocessing import Process, Pipe, Queue

import src.search_engine.bloc_working as bw
import src.search_engine.sub_steps.alphabet_repartition as alp
import src.other.memory_usage as mem


# TODO: comment / docstring all functions
# TODO: bigrams
# TODO: (mini summary for each text) (NOT MANDATORY)
# TODO: args for exec / Makefile
# https://openclassrooms.com/courses/apprenez-a-programmer-en-python/un-peu-de-programmation-systeme#/id/r-2555629
# TODO: process to look at memory usage on all processes
# TODO: doc how-to-use-?
# TODO: relevant ? try proposed queries
# TODO: erase doc with terms after "-"


def main():
    nb_docs_to_look_at = 100
    depth = 3
    groups_nb = 27
    index_nb_docs = 2000
    query = None
    memory_tracker = False

    parser = argparse.ArgumentParser()
    parser.add_argument("--work_to_do",
                        help="alphabet repartition ('alpha') or index creation ('index') or search engine usage ('query')")
    parser.add_argument("--memory_tracker", type=bool, help="memory tracker presence (True) or absence (False)")
    # *------------------------------------------*
    parser.add_argument("--alpha_nb_docs", type=int,
                        help="number of documents to look at to estimate alphabet repartition")
    parser.add_argument("--alpha_depth", type=int, help="number of first letters to look at for alphabet repartition")
    parser.add_argument("--alpha_groups_nb", type=int, help="number of groups for alphabet repartition")
    # *------------------------------------------*
    parser.add_argument("--index_nb_docs", type=int, help="number of docs to index")
    # *------------------------------------------*
    parser.add_argument("--query_query", help="query in natural language")
    args = parser.parse_args()

    if args.work_to_do:
        work_to_do = args.work_to_do
        if args.alpha_nb_docs:
            nb_docs_to_look_at = args.alpha_nb_docs
        if args.alpha_depth:
            depth = args.alpha_depth
        if args.alpha_groups_nb:
            groups_nb = args.alpha_groups_nb
        if args.index_nb_docs:
            index_nb_docs = args.index_nb_docs
        if args.query_query:
            query = args.query_query
        # *------------------------------------------*
        if work_to_do == "alpha":
            alp.alphabet_repartition(nb_docs_to_look_at, depth, groups_nb, memory_tracker)
        elif work_to_do == "index":
            bw.indexes_creation(index_nb_docs)
        elif work_to_do == "query":
            if query == "BENCHMARK":
                bw.test_queries()
            else:
                bw.query(query)
        else:
            print("Error:", work_to_do, "is not a correct name for a job.")
            return -1
    else:
        print("Error: no work to do!")
        return -1

    # bloc_num = 0e
    # sub_bloc_num = 2
    # path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(bloc_num,
    #                                                        bloc_num, sub_bloc_num,
    #                                                        bloc_num, sub_bloc_num)
    # word_num_dict = pck.pickle_load(path_name, "")
    # print(word_num_dict)


if __name__ == '__main__':
    time_gap = 0.01
    q = Queue()
    p = Process(target=mem.track_memory_usage, args=(time_gap, q))
    p.start()

    t_start = time.time()
    main()
    t_end = time.time()

    q.put("STOP_SIGNAL!")
    p.join()

    print("Running time = {} second(s)\n".format(t_end - t_start))

    # mem.plot_memory_usage()
