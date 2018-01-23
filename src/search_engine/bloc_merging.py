import src.other.memory_usage as mem
import src.other.pickle_usage as pck

import os
from multiprocessing import Process, Pipe
from os import remove


def merge_num_name_dict(bloc_num):
    """
    explicit, merge num_name_dict from bloc_num with num_name_dict for master bloc 0
    :param bloc_num:
    :return: nothing all results are stored
    """
    # -- num_name_dict --
    path_name = "b_{}/num_name_dict_b{}".format(0, 0)
    num_name_dict = pck.pickle_load(path_name, "")
    path_name_2 = "b_{}/num_name_dict_b{}".format(bloc_num, bloc_num)
    num_name_dict_2 = pck.pickle_load(path_name_2, "")
    bloc_size = len(num_name_dict)

    for docnum_key_2, name_value_2 in num_name_dict_2.items():
        num_name_dict[bloc_size + docnum_key_2] = name_value_2

    print("merge_num_name_dict() : Memory usage", mem.memory_usage(), "Mo")
    del num_name_dict_2

    remove("data/pickle_files/" + path_name + ".pickle")
    remove("data/pickle_files/" + path_name_2 + ".pickle")
    pck.pickle_store(path_name, num_name_dict, "")
    del num_name_dict


def merge_infos_doc_dict(bloc_num, connection):
    """
    explicit, merge infos_doc_dict from bloc_num with infos_doc_dict for master bloc 0
    :param bloc_num: index of the bloc needed to be merged with the master bloc 0
    :param connection: connection to return the total number of docs in the master bloc 0
    :return: nothing all results are stored
    """
    # -- infos_doc_dict --
    path_name = "b_{}/infos_doc_dict_b{}".format(0, 0)
    infos_doc_dict = pck.pickle_load(path_name, "")
    path_name_2 = "b_{}/infos_doc_dict_b{}".format(bloc_num, bloc_num)
    infos_doc_dict_2 = pck.pickle_load(path_name_2, "")
    bloc_size = len(infos_doc_dict)

    for docnum_key_2, infos_value_2 in infos_doc_dict_2.items():
        infos_doc_dict[bloc_size + docnum_key_2] = infos_value_2

    print("merge_infos_doc_dict() : Memory usage", mem.memory_usage(), "Mo")
    del infos_doc_dict_2

    remove("data/pickle_files/" + path_name + ".pickle")
    remove("data/pickle_files/" + path_name_2 + ".pickle")
    pck.pickle_store(path_name, infos_doc_dict, "")
    del infos_doc_dict

    # Return nb_docs for b0
    if connection:
        connection.send(bloc_size)
        connection.close()
    else:
        return ""


def merge_index_wn_nw_dicts(bloc_num, sub_bloc_num, nb_docs_b0):
    """
    Because the merging of index_dict, num_word_dict, word_num_dict is linked, we need to merge them in one time
    :param bloc_num: index of the bloc needed to be merged with the master bloc 0
    :param sub_bloc_num: index of the sub_bloc needed to be merged with the master sub_bloc 0
    :param nb_docs_b0: we need the total number of docs in the master bloc 0
    :return: nothing all results are stored
    """
    # *------------------------------------------*
    # loading 0
    path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(0,
                                                           0, sub_bloc_num,
                                                           0, sub_bloc_num)
    word_num_dict = pck.pickle_load(path_name, "")
    path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(0,
                                                           0, sub_bloc_num,
                                                           0, sub_bloc_num)
    num_word_dict = pck.pickle_load(path_name, "")
    path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(0,
                                                        0, sub_bloc_num,
                                                        0, sub_bloc_num)
    index_dict = pck.pickle_load(path_name, "")

    # *------------------------------------------*
    # loading bloc_num
    path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(bloc_num,
                                                           bloc_num, sub_bloc_num,
                                                           bloc_num, sub_bloc_num)
    num_word_dict_2 = pck.pickle_load(path_name, "")
    path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(bloc_num,
                                                        bloc_num, sub_bloc_num,
                                                        bloc_num, sub_bloc_num)
    index_dict_2 = pck.pickle_load(path_name, "")

    word_nb = len(word_num_dict)

    for wordnum_key_2, dict_value_2 in index_dict_2.items():
        norm_word = num_word_dict_2[wordnum_key_2]
        word_num = word_num_dict.get(norm_word, -1)

        # word NOT YET in the index
        if word_num < 0:
            word_num_dict[norm_word] = word_nb
            num_word_dict[word_nb] = norm_word
            index_dict[word_nb] = {}

            for docnum_key_2, pos_count_value_2 in dict_value_2.items():
                docnum = nb_docs_b0 + docnum_key_2  # DOCNUM MISTAKE PATCHED
                index_dict[word_nb] = {**index_dict[word_nb], **{docnum: pos_count_value_2}}
            word_nb += 1

        # word ALREADY in the index
        else:
            for docnum_key_2, pos_count_value_2 in dict_value_2.items():
                docnum = nb_docs_b0 + docnum_key_2  # DOCNUM MISTAKE PATCHED
                index_dict[word_num] = {**index_dict[word_num], **{docnum: pos_count_value_2}}

    print("merge_index_wn_nw_dicts() : Memory usage", mem.memory_usage(), "Mo")
    del index_dict_2
    del num_word_dict_2

    # *------------------------------------------*
    # storing index_dict
    path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(bloc_num,
                                                        bloc_num, sub_bloc_num,
                                                        bloc_num, sub_bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(0,
                                                        0, sub_bloc_num,
                                                        0, sub_bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    pck.pickle_store(path_name, index_dict, "")
    del index_dict

    # *------------------------------------------*
    # storing word_num_dict
    path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(bloc_num,
                                                           bloc_num, sub_bloc_num,
                                                           bloc_num, sub_bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(0,
                                                           0, sub_bloc_num,
                                                           0, sub_bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    pck.pickle_store(path_name, word_num_dict, "")
    del word_num_dict

    # *------------------------------------------*
    # storing num_word_dict
    path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(bloc_num,
                                                           bloc_num, sub_bloc_num,
                                                           bloc_num, sub_bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(0,
                                                           0, sub_bloc_num,
                                                           0, sub_bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    pck.pickle_store(path_name, num_word_dict, "")
    del num_word_dict

    os.rmdir("data/pickle_files/b_{}/b_{}_{}".format(bloc_num, bloc_num, sub_bloc_num))


def bloc_merging(bloc_num):
    """
    Merge one bloc of dicts which have been calculated previously for only one databloc.
    after the bloc zero will be calculated for previous bloc zero AND this last databloc.
    in the bloc different things need to be merged :
    -> num_name_dict
    -> infos_doc_dict
    -> index_dict, num_word_dict, word_num_dict
    :param bloc_num: index of the bloc needed to be merged with the master bloc 0
    :return: nothing, results are stored
    """

    # *------------------------------------------*
    # -- num_name_dict --
    p = Process(target=merge_num_name_dict,
                args=(bloc_num,))
    p.start()
    p.join()

    # *------------------------------------------*
    # -- infos_doc_dict --
    # here we need the number of docs for the next split
    parent_conn, child_conn = Pipe()
    p = Process(target=merge_infos_doc_dict,
                args=(bloc_num, child_conn))
    p.start()
    nb_docs_b0 = parent_conn.recv()
    p.join()

    # *------------------------------------------*
    # -- index_dict, num_word_dict, word_num_dict --
    sub_bloc_num = 0
    while os.path.isdir("data/pickle_files/b_0/b_0_{}".format(sub_bloc_num)):
        p = Process(target=merge_index_wn_nw_dicts,
                    args=(bloc_num, sub_bloc_num, nb_docs_b0))
        p.start()
        p.join()
        sub_bloc_num += 1


if __name__ == '__main__':
    pass
