from core_functions import Const
from math import log10


def tf_function(positions_list, infos_doc):
    """
    More infos https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2
    :param positions_list:
    :param infos_doc:
    :return:
    """

    nb_total_words = infos_doc[0]
    term_freq_max = infos_doc[1]

    if Const.TF_WEIGHT == 'binary':
        return 1
    elif Const.TF_WEIGHT == 'raw_count':
        return len(positions_list)
    elif Const.TF_WEIGHT == 'term_frequency':
        return len(positions_list) / nb_total_words
    elif Const.TF_WEIGHT == 'log_frequency':
        return 1 + log10(len(positions_list))
    elif Const.TF_WEIGHT == 'double_normal_05':
        return 0.5 + 0.5 * (len(positions_list)/term_freq_max)
    else:
        raise Exception('Issue with TF calculation: {}'.format(Const.TF_WEIGHT))


def idf_function(word_dict, infos_doc_dict):
    """
    More infos https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency_2
    :param word_dict:
    :param infos_doc_dict:
    :return:
    """

    N_total_docs = len(infos_doc_dict)
    n_docs_term = len(word_dict)
    Ndocs_for_a_word_max = Const.NDOCS_FOR_A_WORD_MAX

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

    for wordnum in index_dict.keys():
        word_dict = index_dict.get(wordnum)

        idf = idf_function(word_dict, infos_doc_dict)
        tf_idf_word_dict = {}

        for document in word_dict.keys():
            positions_list = word_dict.get(document)
            tf = tf_function(positions_list, infos_doc_dict[document])

            tf_idf_word_dict[document] = tf * idf

        tf_idf_dict[wordnum] = tf_idf_word_dict
    return tf_idf_dict


if __name__ == '__main__':
    pass