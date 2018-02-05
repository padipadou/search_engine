import time
import argparse
import os
from multiprocessing import Process, Pipe, Queue

import src.search_engine.bloc_working as bw
import src.search_engine.sub_steps.alphabet_repartition as alp
import src.other.memory_usage as mem
import src.word2vec.test_word2vec as w2v_t

# TODO: working on 1M5 docs
# TODO: argparser for crawler

# TODO: n_grams with position (NOT MANDATORY)
# TODO: (mini summary for each text) (NOT MANDATORY)
# TODO: erase doc with terms after "-" (NOT MANDATORY)
# TODO: relevant ? try proposed queries (NOT MANDATORY)


def str_to_bool(value):
    """
    explicit
    :param value:
    :return:
    """
    if value == "True" or value == "true":
        return True
    else:
        return False

def main():
    """
    complete function understanding parameters
    :return:
    """
    nb_docs_to_look_at = 100
    depth = 3
    groups_nb = 27
    index_nb_docs = 2000
    query = None
    memory_tracker = False

    parser = argparse.ArgumentParser()
    parser.add_argument("--work_to_do",
                        help="alphabet repartition ('alpha') or index creation ('index') or search engine usage ('query') or word2vec test ('w2vtest')")
    parser.add_argument("--memory_tracker", help="memory tracker presence (True) or absence (False)")
    # *------------------------------------------*
    parser.add_argument("--alpha_nb_docs", type=int,
                        help="number of documents to look at to estimate alphabet repartition")
    parser.add_argument("--alpha_depth", type=int, help="number of first letters to look at for alphabet repartition")
    parser.add_argument("--alpha_groups_nb", type=int, help="number of groups for alphabet repartition")
    # *------------------------------------------*
    parser.add_argument("--index_nb_docs", type=int, help="number of docs to index")
    # *------------------------------------------*
    parser.add_argument("--query_query", help="query in natural language")
    # *------------------------------------------*
    parser.add_argument("--mem_plot_phase", help="phase to plot to see memory usage")
    # *------------------------------------------*
    parser.add_argument("--word_to_test", help="word which we need synonyms")
    args = parser.parse_args()

    if args.work_to_do:
        work_to_do = args.work_to_do
        memory_tracker = str_to_bool(args.memory_tracker)

        if work_to_do == "alpha":
            if args.alpha_nb_docs:
                nb_docs_to_look_at = args.alpha_nb_docs
            if args.alpha_depth:
                depth = args.alpha_depth
            if args.alpha_groups_nb:
                groups_nb = args.alpha_groups_nb
            alp.alphabet_repartition(nb_docs_to_look_at, depth, groups_nb, memory_tracker)

        elif work_to_do == "index":
            if args.index_nb_docs:
                index_nb_docs = args.index_nb_docs
            if not os.path.isfile('data/pickle_files/start_end_groups.pickle'):
                print("Error: need a repartition file first, please run the first step.")
                return -1
            bw.indexes_creation(index_nb_docs, memory_tracker)

        elif work_to_do == "query":
            if args.query_query:
                query = args.query_query
            if query == "BENCHMARK":
                bw.test_queries(memory_tracker)
            else:
                bw.query(query, memory_tracker)

        elif work_to_do == "mem_plot":
            if args.mem_plot_phase:
                phase_name = args.mem_plot_phase
            if not os.path.isfile('data/pickle_files/memory_usage_{}.pickle'.format(phase_name)):
                print("Error: need a memory file to plot, please run a code with memory tracker activated first or with a correct filename.")
                return -1
            mem.plot_memory_usage(phase_name)

        elif work_to_do == "w2vtest":
            if args.word_to_test:
                positive_word = args.word_to_test
            w2v_t.word2vec_main(positive_word)

        else:
            print("Error:", work_to_do, "is not a correct name for a job.")
            return -1
    else:
        print("Error: no work to do!")
        return -1


if __name__ == '__main__':
    t_start = time.time()
    main()
    t_end = time.time()

    print("\nRunning time = {} second(s)\n".format(t_end - t_start))
