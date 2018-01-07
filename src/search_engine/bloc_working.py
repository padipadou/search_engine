import src.search_engine.bloc_merging as bm
import src.search_engine.bloc_splitting as bs
import src.search_engine.sub_steps.bm25 as bm25
import src.search_engine.sub_steps.tf_idf as ti
import src.search_engine.sub_steps.index_data as id

import src.other.memory_usage as mem
import src.other.pickle_usage as pck

import os
from multiprocessing import Process, Pipe, Queue


# Before the query, requires some time
def indexes_creation(nb_total_docs, memory_tracker):
    if memory_tracker:
        print("Memory tracker activated.")
        time_gap = 0.01
        phase_name = "index_creation"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

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

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()

    # *------------------------------------------*
    if memory_tracker:
        phase_name = "index_splitting"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

    print("Splitting indexes...", mem.memory_usage(), "Mo")
    start_end_groups = pck.pickle_load("start_end_groups", "") #NEED A TEST AT BEGINNING
    bloc_num = 0
    while os.path.isdir("data/pickle_files/b_{}".format(bloc_num)):
        p = Process(target=bs.split_indexes,
                    args=(bloc_num, start_end_groups))
        p.start()
        p.join()

        bloc_num += 1

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()

    # *------------------------------------------*
    if memory_tracker:
        phase_name = "index_merging"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

    print("Merging indexes...", mem.memory_usage(), "Mo")
    bloc_num = 1
    while os.path.isdir("data/pickle_files/b_{}".format(bloc_num)):
        p = Process(target=bm.bloc_merging,
                    args=(bloc_num,))
        p.start()
        p.join()

        bloc_num += 1

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()

    # *------------------------------------------*
    if memory_tracker:
        phase_name = "tf_idf_calculus"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

    print("Calculating tf * idf...", mem.memory_usage(), "Mo")
    sub_bloc_num = 0
    while os.path.isdir("data/pickle_files/b_{}/b_{}_{}".format(0,
                                                                0, sub_bloc_num)):
        p = Process(target=ti.calculate_tf_idf,
                    args=(sub_bloc_num,))
        p.start()
        p.join()

        sub_bloc_num += 1

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()


# Only the query, requires first step already completed
def query(query=None, memory_tracker=False):
    if memory_tracker:
        print("Memory tracker activated.")
        time_gap = 0.01
        phase_name = "query"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

    start_end_groups = pck.pickle_load("start_end_groups", "") #NEED A TEST
    if query is None:
        query = "israël jérusalem"
        query = "président hollande"

    docnum_score_sum_dict = \
        bm25.bm25(query, start_end_groups)

    path_name = "b_{}/num_name_dict_b{}".format(0, 0)
    num_name_dict = pck.pickle_load(path_name, "")

    text = ""
    text += "\tResults for the query: {}".format(query)
    print(text)
    for key, value in sorted(docnum_score_sum_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print("{}: \t{}".format(num_name_dict[key], value))
        text += "\n{}: \t{}".format(num_name_dict[key], value)

    text += "\n\n"

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()

    return text


def test_queries(memory_tracker):
    if memory_tracker:
        print("Memory tracker activated.")
        time_gap = 0.01
        phase_name = "test_query"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

    text = ""
    text += query("Charlie Hebdo")
    text += query("volcan")
    text += query("playoffs NBA")
    text += query("accidents d'avion")
    text += query("laïcité")
    text += query("élections législatives")
    text += query("Sepp Blatter")
    text += query("budget de la défense")
    text += query("Galaxy S6")
    text += query("Kurdes")

    with open("data/results.txt", "w", encoding='utf8') as file:
        file.write(text)

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()


if __name__ == '__main__':
    pass
