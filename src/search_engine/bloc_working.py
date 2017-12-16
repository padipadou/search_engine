import os
from multiprocessing import Process, Pipe
from os import remove

import src.tf_idf as ti

import src.search_engine.pickle_usage as pck


def split_indexes(bloc_num, start_end_groups): #MAYBE NEED TO IMPROVED WITH PROCESSES

    depth = len(start_end_groups[0][0])

    path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
    index_dict = pck.pickle_load(path_name, "")
    path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
    word_num_dict = pck.pickle_load(path_name, "")

    for sub_bloc_num, start_end_group in enumerate(start_end_groups):
        os.mkdir("data/pickle_files/b_{}/b_{}_{}".format(bloc_num, bloc_num, sub_bloc_num))
        sub_index_dict = {}
        sub_word_num_dict = {}
        sub_num_word_dict = {}

        # we have some letters
        if start_end_group[0] != "0others":
            start_key = start_end_group[0]
            end_key = start_end_group[1]
        # other words
        else:
            start_key = False
            end_key = False

        #useless to sort...
        sorted_items = sorted(word_num_dict.items(), key=lambda x: x[0], reverse=False)
        for key, value in sorted_items:
            if start_key and end_key:
                first_letters = key[:depth]
                if start_key <= first_letters <= end_key:
                    need_to_add = True
                else:
                    need_to_add = False
            else:
                need_to_add = True

            if need_to_add:
                sub_word_num_dict[key] = value
                sub_num_word_dict[value] = key
                sub_index_dict[value] = index_dict[value]
                del word_num_dict[key]

        # print("Memory usage", memory_usage(), "Mo", start_key)

        path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(bloc_num,
                                                                bloc_num, sub_bloc_num,
                                                                bloc_num, sub_bloc_num)
        pck.pickle_store(path_name, sub_word_num_dict, "")
        path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(bloc_num,
                                                                bloc_num, sub_bloc_num,
                                                                bloc_num, sub_bloc_num)
        pck.pickle_store(path_name, sub_num_word_dict, "")
        path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(bloc_num,
                                                                bloc_num, sub_bloc_num,
                                                                bloc_num, sub_bloc_num)
        pck.pickle_store(path_name, sub_index_dict, "")

    path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/num_word_dict_b{}".format(bloc_num, bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")


def merge_num_name_dict(bloc_num):
    # -- num_name_dict --
    path_name = "b_{}/num_name_dict_b{}".format(0, 0)
    num_name_dict = pck.pickle_load(path_name, "")
    path_name_2 = "b_{}/num_name_dict_b{}".format(bloc_num, bloc_num)
    num_name_dict_2 = pck.pickle_load(path_name_2, "")
    bloc_size = len(num_name_dict)

    for docnum_key_2, name_value_2 in num_name_dict_2.items():
        num_name_dict[bloc_size + docnum_key_2] = name_value_2

    print("merge_num_name_dict() : Memory usage", memory_usage(), "Mo")
    del num_name_dict_2

    remove("data/pickle_files/" + path_name + ".pickle")
    remove("data/pickle_files/" + path_name_2 + ".pickle")
    pck.pickle_store(path_name, num_name_dict, "")
    del num_name_dict


def merge_infos_doc_dict(bloc_num, connection):
    # -- infos_doc_dict --
    path_name = "b_{}/infos_doc_dict_b{}".format(0, 0)
    infos_doc_dict = pck.pickle_load(path_name, "")
    path_name_2 = "b_{}/infos_doc_dict_b{}".format(bloc_num, bloc_num)
    infos_doc_dict_2 = pck.pickle_load(path_name_2, "")
    bloc_size = len(infos_doc_dict)

    for docnum_key_2, infos_value_2 in infos_doc_dict_2.items():
        infos_doc_dict[bloc_size + docnum_key_2] = infos_value_2

    print("merge_infos_doc_dict() : Memory usage", memory_usage(), "Mo")
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
    # *------------------------------------------*
    # 0
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
    # bloc_num
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
                docnum = nb_docs_b0 + docnum_key_2 #DOCNUM MISTAKE PATCHED
                index_dict[word_nb] = {**index_dict[word_nb], **{docnum: pos_count_value_2}}
            word_nb += 1

        # word ALREADY in the index
        else:
            for docnum_key_2, pos_count_value_2 in dict_value_2.items():
                docnum = nb_docs_b0 + docnum_key_2 #DOCNUM MISTAKE PATCHED
                index_dict[word_num] = {**index_dict[word_num], **{docnum: pos_count_value_2}}

    print("merge_index_wn_nw_dicts() : Memory usage", memory_usage(), "Mo")
    del index_dict_2
    del num_word_dict_2

    # *------------------------------------------*
    # index_dict
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
    # word_num_dict
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
    # num_word_dict
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
    # """
    # Merge 2 blocs which have been already created
    # In order to make a clear distinction:
    # -> each variable linked to bloc_num1 are suffixed by '_1'
    # -> each variable linked to bloc_num2 are suffixed by '_2'
    # -> each variable linked to the final bloc are NOT suffixed
    # :param bloc_num1: number to identify first bloc to merge among others
    # :param bloc_num2: number to identify second bloc to merge among others
    # :return: nothing
    # """

    # *------------------------------------------*
    p = Process(target=merge_num_name_dict,
                args=(bloc_num,))
    p.start()
    p.join()

    # *------------------------------------------*
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


def calculate_tf_idf(sub_bloc_num):
    # *------------------------------------------*
    # Loading
    path_name = "b_{}/infos_doc_dict_b{}".format(0, 0)
    infos_doc_dict = pck.pickle_load(path_name, "")

    path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(0,
                                                        0, sub_bloc_num,
                                                        0, sub_bloc_num)
    index_dict = pck.pickle_load(path_name, "")

    # *------------------------------------------*
    # Calculation
    tf_idf_dict, tf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)
    print("calculate_tf_idf() : Memory usage", memory_usage(), "Mo")

    del index_dict
    del infos_doc_dict

    # *------------------------------------------*
    # Storing values
    remove("data/pickle_files/" + path_name + ".pickle")

    path_name = "b_{}/b_{}_{}/tf_dict_b{}_{}".format(0,
                                                     0, sub_bloc_num,
                                                     0, sub_bloc_num)
    pck.pickle_store(path_name, tf_dict, "")
    del tf_dict

    path_name = "b_{}/b_{}_{}/tf_idf_dict_b{}_{}".format(0,
                                                     0, sub_bloc_num,
                                                     0, sub_bloc_num)
    pck.pickle_store(path_name, tf_idf_dict, "")
    del tf_idf_dict


if __name__ == '__main__':
    pass
