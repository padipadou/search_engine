import libs.kea as kea
import Stemmer as pystemmer
from core_functions import Const


def bm25_function(query, stopwords, word_num_dict, tf_idf_dict, tf_dict, infos_doc_dict):
    """
    More info https://en.wikipedia.org/wiki/Okapi_BM25
    :param query:
    :param stopwords:
    :return:
    """
    k1 = 1.5
    b = 0.75
    nb_words_avg = 0
    for value in infos_doc_dict.values():
        nb_words_avg += value[0]
    nb_words_avg /= len(infos_doc_dict)

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    # stemmer, from PyStemmer
    stemmer = pystemmer.Stemmer('french')

    #query_list = []
    words_query = tokenizer.tokenize(query)

    keyword_num_list = []

    for word in words_query:
        if word not in stopwords:
            if Const.STEMMER == True:
                wordstem = stemmer.stemWord(word).lower()
            else:
                wordstem = word.lower()

            keyword_num = word_num_dict.get(wordstem, -1)
            if keyword_num >= 0:
                keyword_num_list.append(keyword_num)

    docnum_score_sum_dict = {}
    for keyword_num in keyword_num_list:
        keyword_docnums_tf_idf_dict = tf_idf_dict[keyword_num]

        for docnum_key in keyword_docnums_tf_idf_dict.keys():
            tf_idf = keyword_docnums_tf_idf_dict[docnum_key]
            nb_words = infos_doc_dict[docnum_key][0]
            docnum_score_sum = docnum_score_sum_dict.get(docnum_key, 0)
            tf = tf_dict[keyword_num][docnum_key]

            score = tf_idf * (k1 + 1) \
                    / (tf + k1 * (1 - b + b * (nb_words / nb_words_avg)))

            docnum_score_sum_dict[docnum_key] = docnum_score_sum + score

    return docnum_score_sum_dict


if __name__ == '__main__':
    pass