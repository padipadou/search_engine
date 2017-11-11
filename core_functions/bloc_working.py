import os
import core_functions.pickle_usage as pck
import core_functions.handle_data as hd
import core_functions.index_data as idxd
from core_functions import Const


def bloc_indexing(bloc_num, size_bloc=10000):
    """
    Create and store num_name_dict, index_dict, word_num_dict, num_word_dict, infos_doc_dict for one bloc
    :param bloc_num: number to identify each bloc among others
    :param size_bloc: number of documents per bloc
    :return: nothing
    """
    # print("Loading data...")
    data_dict, name_num_dict, num_name_dict = \
        hd.load_data_dict(Const.DIRECTORY_NAME, size_bloc, bloc_num * size_bloc)

    # useful ?
    del name_num_dict

    # useful ?
    pck.pickle_store("num_name_dict_b" + str(bloc_num), num_name_dict, "")
    del num_name_dict

    stopwords = hd.load_stopwords_set()

    # *------------------------------------------*
    # print("Creating index...")
    index_dict, word_num_dict, num_word_dict, infos_doc_dict = \
        idxd.create_index_dict(data_dict, stopwords)

    del data_dict
    del stopwords

    pck.pickle_store("index_dict_b" + str(bloc_num), index_dict, "")
    del index_dict

    pck.pickle_store("word_num_dict_b" + str(bloc_num), word_num_dict, "")
    del word_num_dict

    pck.pickle_store("num_word_dict_b" + str(bloc_num), num_word_dict, "")
    del num_word_dict

    pck.pickle_store("infos_doc_dict_b" + str(bloc_num), infos_doc_dict, "")
    del infos_doc_dict


def bloc_merging(bloc_num1, bloc_num2, blocsize):
    """
    Merge 2 blocs which have been already created
    In order to make a clear distinction:
    -> each variable linked to bloc_num1 are suffixed by '_1'
    -> each variable linked to bloc_num2 are suffixed by '_2'
    -> each variable linked to the final bloc are NOT suffixed
    :param bloc_num1: number to identify first bloc to merge among others
    :param bloc_num2: number to identify second bloc to merge among others
    :param blocsize: size of blocs (number of docs)
    :return: nothing
    """
    # *------------------------------------------*
    # -- num_name_dict --
    num_name_dict = pck.pickle_load("num_name_dict_b" + str(bloc_num1), "")
    num_name_dict_2 = pck.pickle_load("num_name_dict_b" + str(bloc_num2), "")

    for docnum_key_2, name_value_2  in num_name_dict_2.items():
        num_name_dict[blocsize + docnum_key_2] = name_value_2

    del num_name_dict_2

    os.remove("data/pickle_files/num_name_dict_b" + str(bloc_num1) + ".pickle")
    os.remove("data/pickle_files/num_name_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("num_name_dict_b" + str(bloc_num1), num_name_dict, "")
    del num_name_dict

    # *------------------------------------------*
    # -- index_dict, num_word_dict, word_num_dict --
    index_dict = pck.pickle_load("index_dict_b" + str(bloc_num1), "")
    word_num_dict = pck.pickle_load("word_num_dict_b" + str(bloc_num1), "")
    num_word_dict = pck.pickle_load("num_word_dict_b" + str(bloc_num1), "")

    i_newword = len(word_num_dict) + 0

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
                docnum = blocsize + docnum_key_2
                index_dict[i_newword] = {**index_dict[i_newword], **{docnum: pos_count_value_2}}
            i_newword += 1

        # word ALREADY in the index
        else:
            for docnum_key_2, pos_count_value_2 in dict_value_2.items():
                docnum = blocsize + docnum_key_2
                index_dict[word_num] = {**index_dict[word_num], **{docnum: pos_count_value_2}}

    del index_dict_2
    del num_word_dict_2

    os.remove("data/pickle_files/index_dict_b" + str(bloc_num1) + ".pickle")
    os.remove("data/pickle_files/index_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("index_dict_b" + str(bloc_num1), index_dict, "")
    del index_dict

    os.remove("data/pickle_files/word_num_dict_b" + str(bloc_num1) + ".pickle")
    os.remove("data/pickle_files/word_num_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("word_num_dict_b" + str(bloc_num1), word_num_dict, "")
    del word_num_dict

    os.remove("data/pickle_files/num_word_dict_b" + str(bloc_num1) + ".pickle")
    os.remove("data/pickle_files/num_word_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("num_word_dict_b" + str(bloc_num1), num_word_dict, "")
    del num_word_dict

    # *------------------------------------------*
    # -- infos_doc_dict --
    infos_doc_dict = pck.pickle_load("infos_doc_dict_b" + str(bloc_num1), "")
    infos_doc_dict_2 = pck.pickle_load("infos_doc_dict_b" + str(bloc_num2), "")

    for docnum_key_2, infos_value_2  in infos_doc_dict_2.items():
        infos_doc_dict[blocsize + docnum_key_2] = infos_value_2

    del infos_doc_dict_2

    os.remove("data/pickle_files/infos_doc_dict_b" + str(bloc_num1) + ".pickle")
    os.remove("data/pickle_files/infos_doc_dict_b" + str(bloc_num2) + ".pickle")
    pck.pickle_store("infos_doc_dict_b" + str(bloc_num1), infos_doc_dict, "")
    del infos_doc_dict


if __name__ == '__main__':
    pass