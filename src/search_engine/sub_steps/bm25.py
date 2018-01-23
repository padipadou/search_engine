import src.other.pickle_usage as pck
import src.search_engine.sub_steps.handle_data as hd
import src.search_engine.sub_steps.normalization  as nrm
from src import Const
import libs.kea as kea

import Stemmer as pystemmer


def get_sub_bloc_num_dict(words_query, start_end_groups):
    sub_bloc_num_dict = {}
    stopwords = hd.load_stopwords_set()
    depth = 3

    # stemmer, from PyStemmer
    if Const.STEMMER is True:
        stemmer = pystemmer.Stemmer('french')
    else:
        stemmer = None

    for word in words_query:
        norm_word = nrm.normalization(word, stopwords, stemmer)
        if norm_word is not None:
            for sub_bloc_num, start_end_group in enumerate(start_end_groups):
                # we have some letters
                if start_end_group[0] != "0others":
                    start_key = start_end_group[0]
                    end_key = start_end_group[1]
                    first_letters = norm_word[:depth]

                    # word is here
                    if start_key <= first_letters <= end_key:
                        need_to_add = True
                    # word is still not here
                    else:
                        need_to_add = False

                # other words,  last category, in default
                else:
                    start_key = False
                    end_key = False
                    need_to_add = True

                if need_to_add:
                    if sub_bloc_num_dict.get(sub_bloc_num) is None:
                        sub_bloc_num_dict[sub_bloc_num] = []
                    sub_bloc_num_dict[sub_bloc_num].append(norm_word)
                    continue

    return sub_bloc_num_dict


def get_nb_words_avg(infos_doc_dict):
    nb_words_avg = 0
    for value in infos_doc_dict.values():
        nb_words_avg += value[0]
    nb_words_avg /= len(infos_doc_dict)

    return nb_words_avg


def get_keyword_num_list(words_query, word_num_dict):
    """

    :param words_query:
    :param word_num_dict:
    :return:
    """
    keyword_num_list = []

    for norm_word in words_query:
        keyword_num = word_num_dict.get(norm_word, -1)
        if keyword_num >= 0:
            keyword_num_list.append(keyword_num)

    return keyword_num_list


def bm25(query, start_end_groups):
    """
    BM25 done into ONE process reaching index splitted by blocs
    More info https://en.wikipedia.org/wiki/Okapi_BM25
    :param query: normal sentence in natural language
    :param start_end_groups: list of list with start_key, prev_key, number of words, percentage
    :return: dict with docnum as key, score of bm25 as value
    """

    docnum_score_sum_dict = {}

    # bm25 parameters
    k1 = 1.5
    b = 0.75

    # COULD BE PUT INTO A PROCESS /!\ (reducing memory, increasing time access ?)
    path_name = "b_{}/infos_doc_dict_b{}".format(0, 0)
    infos_doc_dict = pck.pickle_load(path_name, "")
    nb_words_avg = get_nb_words_avg(infos_doc_dict)

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    words_query = tokenizer.tokenize(query)

    # keyword_num_list = get_keyword_num_list(words_query, word_num_dict, stopwords)
    sub_bloc_num_dict = get_sub_bloc_num_dict(words_query, start_end_groups)

    if len(sub_bloc_num_dict) == 0:
        print("No results in the corpus")
        return docnum_score_sum_dict

    # CAN BE PUT INTO DIFFERENT PROCESSES /!\ (reducing memory, increasing time access ?)
    for sub_bloc_num, words_list in sub_bloc_num_dict.items():
        # loading dicts
        path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(0,
                                                               0, sub_bloc_num,
                                                               0, sub_bloc_num)
        word_num_dict = pck.pickle_load(path_name, "")
        path_name = "b_{}/b_{}_{}/tf_dict_b{}_{}".format(0,
                                                         0, sub_bloc_num,
                                                         0, sub_bloc_num)
        tf_dict = pck.pickle_load(path_name, "")
        path_name = "b_{}/b_{}_{}/tf_idf_dict_b{}_{}".format(0,
                                                             0, sub_bloc_num,
                                                             0, sub_bloc_num)
        tf_idf_dict = pck.pickle_load(path_name, "")

        # traditional bm25
        keyword_num_list = get_keyword_num_list(words_list, word_num_dict)

        for keyword_num in keyword_num_list:
            keyword_docnums_tf_idf_dict = tf_idf_dict[keyword_num]

            for docnum_key in keyword_docnums_tf_idf_dict.keys():
                tf_idf = keyword_docnums_tf_idf_dict[docnum_key]
                nb_words = infos_doc_dict[docnum_key][0]
                docnum_score_sum = docnum_score_sum_dict.get(docnum_key, 0)
                tf = tf_dict[keyword_num][docnum_key]

                # Bm25 score
                score = tf_idf * (k1 + 1) \
                        / (tf + k1 * (1 - b + b * (nb_words / nb_words_avg)))

                # Sum
                docnum_score_sum_dict[docnum_key] = docnum_score_sum + score

        del word_num_dict
        del tf_dict
        del tf_idf_dict

    return docnum_score_sum_dict


if __name__ == '__main__':
    pass
