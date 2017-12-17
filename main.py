import src.search_engine.bloc_working.bloc_working as bw
import src.search_engine.alphabet_repartition as alp
import time


# TODO: comment / docstring all functions
# TODO: bigrams
# TODO: mini summary for each text
# TODO: args for exec / Makefile

def main():
    depth = 3
    groups_nb = 27
    nb_docs_to_look_at = 3000

    alp.alphabet_repartition(nb_docs_to_look_at, depth, groups_nb)
    # bw.indexes_creation(3000)
    # bw.query()

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
