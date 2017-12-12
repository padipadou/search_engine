from os import remove
from math import ceil
import core_functions.pickle_usage as pck
import core_functions.handle_data as hd
import core_functions.index_data as idxd
import core_functions.tf_idf as ti
from core_functions import Const
import psutil
import gc
import os
import time


def memory_usage():
    """
    Return memory usage for the current process in Mo
    :return: memory_usage:
    """
    memory_usage = -1
    pid = os.getpid() # this process pid
    infos = None
    for p in psutil.process_iter(attrs=['pid']):
        if p.info['pid'] == pid:
            infos = p.memory_info()
    if infos:
        # in Mo
        memory_usage = int(infos.rss / (1024 ** 3) * 1000)

    if memory_usage < 0:
        print("Error with memory calculation")
        return -1
    else:
        return memory_usage


def bloc_indexing(i_start_doc, bloc_num, nb_total_docs, connection=None):
    """
    * Create a directory for each bloc with a precise memory size
    * Create and store num_name_dict, index_dict, word_num_dict, num_word_dict, infos_doc_dict for one bloc
    :param i_start_doc: first doc to look at in repertory
    :param bloc_num: number to store each bloc amongst others
    :param nb_total_docs: max number of wanted docs
    :param connection: connection for the process (easiest way to handle memory)
    :return: i_doc: number of docs which has been explorated in this part
    """

    i_doc = i_start_doc
    minibatch_size = 400
    max_memory_usage = 50 #in Mo

    num_name_dict = {}
    infos_doc_dict = {}
    index_dict = {}
    word_num_dict = {}
    num_word_dict = {}

    while i_doc < nb_total_docs and memory_usage() < max_memory_usage:
        data_dict, num_name_dict_temp = \
            hd.load_data_dict(Const.DIRECTORY_NAME, minibatch_size, i_doc)

        print("Memory usage", memory_usage(), "Mo")

        i_doc += len(data_dict)

        i_newdoc = len(num_name_dict)
        i_newword = len(word_num_dict)

        # -- num_name_dict --
        for key, value in num_name_dict_temp.items():
            num_name_dict[i_newdoc + key] = value
        del num_name_dict_temp

        # /!\ word_num_dict_temp useless
        index_dict_temp, word_num_dict_temp, num_word_dict_temp, infos_doc_dict_temp = \
            idxd.create_index_dict(data_dict)
        del data_dict

        # -- infos_doc_dict --
        for key, value in infos_doc_dict_temp.items():
            infos_doc_dict[i_newdoc + key] = value
        del infos_doc_dict_temp

        # -- index_dict, num_word_dict, word_num_dict --
        for wordnum_key_temp, dict_value_temp in index_dict_temp.items():
            norm_word = num_word_dict_temp[wordnum_key_temp]
            word_num = word_num_dict.get(norm_word, -1)

            # word NOT YET in the global index
            if word_num < 0:
                word_num_dict[norm_word] = i_newword
                num_word_dict[i_newword] = norm_word
                index_dict[i_newword] = {}

                for docnum_key_temp, pos_count_value_temp in dict_value_temp.items():
                    docnum = i_newdoc + docnum_key_temp
                    index_dict[i_newword] = {**index_dict[i_newword], **{docnum: pos_count_value_temp}}
                i_newword += 1

            # word ALREADY in the global index
            else:
                for docnum_key_temp, pos_count_value_temp in dict_value_temp.items():
                    docnum = i_newdoc + docnum_key_temp
                    index_dict[word_num] = {**index_dict[word_num], **{docnum: pos_count_value_temp}}

        del index_dict_temp
        del num_word_dict_temp

    # Storing dictionaries
    os.mkdir("data/pickle_files/b_{}".format(bloc_num))
    if num_name_dict and infos_doc_dict and index_dict and word_num_dict and num_word_dict:
        path_name = "b_{}/num_name_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, num_name_dict, "")
        del num_name_dict

        path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, index_dict, "")
        del index_dict

        path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, word_num_dict, "")
        del word_num_dict

        path_name = "b_{}/num_word_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, num_word_dict, "")
        del num_word_dict

        path_name = "b_{}/infos_doc_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, infos_doc_dict, "")
        del infos_doc_dict

    # Return nb_docs done
    if connection:
        connection.send(i_doc)
        connection.close()
    else:
        return i_doc

#DEPRECATED
def bloc_merging(bloc_num1, bloc_num2):
    """
    Merge 2 blocs which have been already created
    In order to make a clear distinction:
    -> each variable linked to bloc_num1 are suffixed by '_1'
    -> each variable linked to bloc_num2 are suffixed by '_2'
    -> each variable linked to the final bloc are NOT suffixed
    :param bloc_num1: number to identify first bloc to merge among others
    :param bloc_num2: number to identify second bloc to merge among others
    :return: nothing
    """
    # *------------------------------------------*
    # -- num_name_dict --
    num_name_dict = pck.pickle_load("num_name_dict_b" + str(bloc_num1), "")
    num_name_dict_2 = pck.pickle_load("num_name_dict_b" + str(bloc_num2), "")
    bloc_size = len(num_name_dict)

    for docnum_key_2, name_value_2 in num_name_dict_2.items():
        num_name_dict[bloc_size + docnum_key_2] = name_value_2

    del num_name_dict_2

    remove("data/pickle_files/num_name_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/num_name_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("num_name_dict_b" + str(bloc_num1), num_name_dict, "")
    del num_name_dict

    # *------------------------------------------*
    # -- index_dict, num_word_dict, word_num_dict --
    index_dict = pck.pickle_load("index_dict_b" + str(bloc_num1), "")
    word_num_dict = pck.pickle_load("word_num_dict_b" + str(bloc_num1), "")
    num_word_dict = pck.pickle_load("num_word_dict_b" + str(bloc_num1), "")

    i_newword = len(word_num_dict)

    index_dict_2 = pck.pickle_load("index_dict_b" + str(bloc_num2), "")
    num_word_dict_2 = pck.pickle_load("num_word_dict_b" + str(bloc_num2), "")
    for wordnum_key_2, dict_value_2 in index_dict_2.items():
        norm_word = num_word_dict_2[wordnum_key_2]
        word_num = word_num_dict.get(norm_word, -1)

        # word NOT YET in the index
        if word_num < 0:
            word_num_dict[norm_word] = i_newword
            num_word_dict[i_newword] = norm_word
            index_dict[i_newword] = {}

            for docnum_key_2, pos_count_value_2 in dict_value_2.items():
                docnum = bloc_size + docnum_key_2
                index_dict[i_newword] = {**index_dict[i_newword], **{docnum: pos_count_value_2}}
            i_newword += 1

        # word ALREADY in the index
        else:
            for docnum_key_2, pos_count_value_2 in dict_value_2.items():
                docnum = bloc_size + docnum_key_2
                index_dict[word_num] = {**index_dict[word_num], **{docnum: pos_count_value_2}}

    del index_dict_2
    del num_word_dict_2

    remove("data/pickle_files/index_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/index_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("index_dict_b" + str(bloc_num1), index_dict, "")
    del index_dict

    remove("data/pickle_files/word_num_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/word_num_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("word_num_dict_b" + str(bloc_num1), word_num_dict, "")
    del word_num_dict

    remove("data/pickle_files/num_word_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/num_word_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("num_word_dict_b" + str(bloc_num1), num_word_dict, "")
    del num_word_dict

    # *------------------------------------------*
    # -- infos_doc_dict --
    infos_doc_dict = pck.pickle_load("infos_doc_dict_b" + str(bloc_num1), "")
    infos_doc_dict_2 = pck.pickle_load("infos_doc_dict_b" + str(bloc_num2), "")
    bloc_size = len(infos_doc_dict)

    for docnum_key_2, infos_value_2 in infos_doc_dict_2.items():
        infos_doc_dict[bloc_size + docnum_key_2] = infos_value_2

    del infos_doc_dict_2

    remove("data/pickle_files/infos_doc_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/infos_doc_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("infos_doc_dict_b" + str(bloc_num1), infos_doc_dict, "")
    del infos_doc_dict

    # num_name_dict     OK
    # index_dict        OK
    # num_word_dict     OK
    # word_num_dict     OK
    # infos_doc_dict    OK

def split_indexes(bloc_num, start_end_groups):

    depth = len(start_end_groups[0][0])

    path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
    index_dict = pck.pickle_load(path_name, "")
    path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
    word_num_dict = pck.pickle_load(path_name, "")

    for i_alpha_rep, start_end_group in enumerate(start_end_groups):
        os.mkdir("data/pickle_files/b_{}/b_{}_{}".format(bloc_num, bloc_num, i_alpha_rep))
        sub_index_dict = {}
        sub_word_num_dict = {}
        sub_num_word_dict = {}

        if start_end_group[0] != "0others":
            start_key = start_end_group[0]
            end_key = start_end_group[1]
        else:
            break

        for key, value in sorted(word_num_dict.items(), key=lambda x: x[0], reverse=False):
            first_letters = key[:depth-1]
            if start_key <= first_letters <= end_key:
                sub_word_num_dict[key] = value
                sub_num_word_dict[value] = key
                sub_index_dict[value] = index_dict[value]

        path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(bloc_num,
                                                                bloc_num, i_alpha_rep,
                                                                bloc_num, i_alpha_rep)
        pck.pickle_store(path_name, sub_word_num_dict, "")
        path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(bloc_num,
                                                                bloc_num, i_alpha_rep,
                                                                bloc_num, i_alpha_rep)
        pck.pickle_store(path_name, sub_num_word_dict, "")
        path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(bloc_num,
                                                                bloc_num, i_alpha_rep,
                                                                bloc_num, i_alpha_rep)
        pck.pickle_store(path_name, sub_index_dict, "")

    # index_dict = pck.pickle_load("index_dict_b0", "")
    # remove("data/pickle_files/index_dict_b0.pickle")
    # index_bloc_len = ceil(len(index_dict) / total_nb_blocs_index)
    #
    # current_index_bloc = 0
    # index_dict_bloc = {}
    # for wordnum in range(len(index_dict)):
    #     # if the bloc is full, need to be stored
    #     if wordnum == (current_index_bloc + 1) * index_bloc_len:
    #         pck.pickle_store("index_dict_b" + str(current_index_bloc), index_dict_bloc, "")
    #         del index_dict_bloc
    #
    #         current_index_bloc += 1
    #         index_dict_bloc = {}
    #
    #     index_dict_bloc[wordnum] = index_dict.get(wordnum)
    #
    # # last bloc, need to be stored
    # pck.pickle_store("index_dict_b" + str(current_index_bloc), index_dict_bloc, "")
    # del index_dict_bloc


def calculate_tf_idf(blocnum, total_nb_blocs_index):
    infos_doc_dict = pck.pickle_load("infos_doc_dict_b0", "")

    index_dict = pck.pickle_load("index_dict_b" + str(blocnum), "")
    tf_idf_dict, tf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)
    del index_dict
    del infos_doc_dict
    remove("data/pickle_files/index_dict_b" + str(blocnum) + ".pickle")

    pck.pickle_store("tf_dict_b" + str(blocnum), tf_dict, "")
    pck.pickle_store("tf_idf_dict_b" + str(blocnum), tf_idf_dict, "")
    del tf_dict
    del tf_idf_dict


def bloc_merging2(bloc_num1, bloc_num2):
    # *------------------------------------------*
    # -- tf_idf_dict --
    tf_idf_dict = pck.pickle_load("tf_idf_dict_b" + str(bloc_num1), "")
    tf_idf_dict_2 = pck.pickle_load("tf_idf_dict_b" + str(bloc_num2), "")
    blocsize = len(tf_idf_dict)

    for wordnum_key_2, dict_value_2 in tf_idf_dict_2.items():
        # tf_idf_dict[blocsize + wordnum_key_2] = dict_value_2
        tf_idf_dict[wordnum_key_2] = dict_value_2

    del tf_idf_dict_2

    remove("data/pickle_files/tf_idf_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/tf_idf_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("tf_idf_dict_b" + str(bloc_num1), tf_idf_dict, "")
    del tf_idf_dict

    # *------------------------------------------*
    # -- tf_dict --
    tf_dict = pck.pickle_load("tf_dict_b" + str(bloc_num1), "")
    tf_dict_2 = pck.pickle_load("tf_dict_b" + str(bloc_num2), "")
    blocsize = len(tf_dict)

    for wordnum_key_2, dict_value_2 in tf_dict_2.items():
        # tf_dict[blocsize + wordnum_key_2] = dict_value_2
        tf_dict[wordnum_key_2] = dict_value_2

    del tf_dict_2

    remove("data/pickle_files/tf_dict_b" + str(bloc_num1) + ".pickle")
    remove("data/pickle_files/tf_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("tf_dict_b" + str(bloc_num1), tf_dict, "")
    del tf_dict


if __name__ == '__main__':
    pass
