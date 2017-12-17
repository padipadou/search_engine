import src.search_engine.pickle_usage as pck
import src.other.memory_usage as mem
from src import Const

from math import log10
from os import remove


def tf_function(positions_or_count, infos_doc):
    """
    More infos https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2
    :param positions_or_count: list of positions one word in the doc or directly the count of words for this word
    :param infos_doc: list[0]: total nb of words, list[1]: term frequency max
    :return: tf_value for this word regarding to differents way of calculation
    """

    nb_total_words = infos_doc[0]
    term_freq_max = infos_doc[1]

    if Const.POSITIONS_LIST is True:
        count = len(positions_or_count)
    else:
        count = positions_or_count

    if Const.TF_WEIGHT == 'binary':
        return 1
    elif Const.TF_WEIGHT == 'raw_count':
        return count
    elif Const.TF_WEIGHT == 'term_frequency':
        return count / nb_total_words
    elif Const.TF_WEIGHT == 'log_frequency':
        return 1 + log10(count)
    elif Const.TF_WEIGHT == 'double_normal_05':
        return 0.5 + 0.5 * (count/term_freq_max)
    else:
        raise Exception('Issue with TF calculation: {}'.format(Const.TF_WEIGHT))


def idf_function(word_dict):
    """
    More infos https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency_2
    :param word_dict: dict with docnum as key, list of positions OR a count per doc as value
    :return: idf_value for this word regarding to differents way of calculation
    """

    N_total_docs = Const.CORPUS_SIZE
    n_docs_term = len(word_dict)
    Ndocs_for_a_word_max = Const.NB_DOCS_FOR_A_WORD_MAX

    if Const.IDF_WEIGHT == 'unary':
        return 1
    elif Const.IDF_WEIGHT == 'idf':
        return log10(N_total_docs/n_docs_term)
    elif Const.IDF_WEIGHT == 'idf_smooth':
        return log10(1 + N_total_docs/n_docs_term)
    elif Const.IDF_WEIGHT == 'idf_max':
        return log10(Ndocs_for_a_word_max/(1 + n_docs_term))
    elif Const.IDF_WEIGHT == 'idf_probalistic':
        return log10((N_total_docs - n_docs_term)/n_docs_term)
    elif Const.IDF_WEIGHT == 'idf_probalistic_05':
        return log10((N_total_docs - n_docs_term + 0.5)/(n_docs_term + 0.5))
    else:
        raise Exception('Issue with IDF calculation: {}'.format(Const.IDF_WEIGHT))


def calculate_tf_idf_dict(index_dict, infos_doc_dict):
    """
    Calculates a dict of words as keys and dicts as values.
    For each dict, you have docnums as keys and tf*idf as values.
    """
    tf_idf_dict = {}
    tf_dict = {}
    Const.CORPUS_SIZE = len(infos_doc_dict)

    # index_dict could be split into different dict if needed
    for wordnum, word_dict in index_dict.items():

        idf = idf_function(word_dict)
        tf_idf_word_dict = {}
        tf_word_dict = {}

        for document in word_dict.keys():
            positions_or_count = word_dict.get(document)
            tf = tf_function(positions_or_count, infos_doc_dict[document])

            tf_idf_word_dict[document] = tf * idf

            if Const.BM_25 is True:
                tf_word_dict[document] = tf

        tf_idf_dict[wordnum] = tf_idf_word_dict
        if Const.BM_25 is True:
            tf_dict[wordnum] = tf_word_dict

    return tf_idf_dict, tf_dict


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
        calculate_tf_idf_dict(index_dict, infos_doc_dict)
    print("calculate_tf_idf() : Memory usage", mem.memory_usage(), "Mo")

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