import time
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


def test_queries():
    bw.query("Charlie Hebdo")
    bw.query("volcan")
    bw.query("playoffs NBA")
    bw.query("accidents d'avion")
    bw.query("laïcité")
    bw.query("élections législatives")
    bw.query("Sepp Blatter")
    bw.query("budget de la défense")
    bw.query("Galaxy S6")
    bw.query("Kurdes")

def main():
    # depth = 3
    # groups_nb = 27
    # nb_docs_to_look_at = 100
    #
    # alp.alphabet_repartition(nb_docs_to_look_at, depth, groups_nb)
    # bw.indexes_creation(2000)
    # bw.query()

    test_queries()

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
