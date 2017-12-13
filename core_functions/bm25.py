import libs.kea as kea
import Stemmer as pystemmer
from core_functions import Const
from core_functions import normalization as nrm

def big_query_bm25()
def bm25_function(query, stopwords,
                  word_num_dict=None,
                  tf_idf_dict=None,
                  tf_dict=None,
                  infos_doc_dict=None,
                  byBloc=False):
    """
    More info https://en.wikipedia.org/wiki/Okapi_BM25
    :param query: normal sentence in natural language
    :param stopwords: set of stopwords
    :param word_num_dict: dict with normalized word as key, wordnum as value
    :param tf_idf_dict: dict with wordnum as key, dict as value (dict with docnum as key, tf*idf as value per doc)
    :param tf_dict: dict with wordnum as key, tf as value
    :param infos_doc_dict: dict with docnum  as key, list as value (per doc; list[0]: total nb of words, list[1]: term frequency max)
    :return: dict with docnum as key, score of bm25 as value
    """
    docnum_score_sum_dict = {}

    if (word_num_dict is None \
        or tf_idf_dict is None \
        or tf_dict is None \
        or infos_doc_dict is None) \
        and byBloc is not True:
        print("Error with arguments in bm25 function.")
        return docnum_score_sum_dict


    # bm25 parameters
    k1 = 1.5
    b = 0.75
    nb_words_avg = get_nb_words_avg(infos_doc_dict)

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    words_query = tokenizer.tokenize(query)

    keyword_num_list = get_keyword_num_list(words_query, word_num_dict, stopwords)

    if len(keyword_num_list) == 0:
        print("No results in the corpus")
        return docnum_score_sum_dict

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

    return docnum_score_sum_dict


def test_dict(tf_idf_dict):
    for i in range(len(tf_idf_dict)):
        test_val = tf_idf_dict.get(i, -1)
        if test_val == -1:
            print(i)


def get_nb_words_avg(infos_doc_dict):
    nb_words_avg = 0
    for value in infos_doc_dict.values():
        nb_words_avg += value[0]
    nb_words_avg /= len(infos_doc_dict)

    return nb_words_avg


def get_keyword_num_list(words_query, word_num_dict, stopwords):
    keyword_num_list = []

    # stemmer, from PyStemmer
    if Const.STEMMER is True:
        stemmer = pystemmer.Stemmer('french')
    else:
        stemmer = None

    for word in words_query:
        norm_word = nrm.normalization(word, stopwords, stemmer)
        if norm_word is not None:
            keyword_num = word_num_dict.get(norm_word, -1)
            if keyword_num >= 0:
                keyword_num_list.append(keyword_num)

    return keyword_num_list


if __name__ == '__main__':
    pass