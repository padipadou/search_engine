import core_functions.load_data as ld
from math import sqrt

def calculate_tf_idf_dict(index_dict):
    """
    Calculates a dict of words as keys and dicts as values.
    For each dict, you have docnums as keys and tf*idf as values.
    """
    tf_idf_dict = {}

    for wordnum in index_dict.keys():
        word_dict = index_dict.get(wordnum)
        idf = 1/len(word_dict)
        tf_idf_word_dict = {}

        for document in word_dict.keys():
            positions_list = word_dict.get(document)
            tf = len(positions_list)
            tf_idf_word_dict[document] = tf * idf

        tf_idf_dict[wordnum] = tf_idf_word_dict
    return tf_idf_dict


def create_doc_vector_dict(docnum, tf_idf_dict):
    """
    Creates and returns a dict linked to a DOC with words as keys in it and the tf*idf as values for each of them.
    WARNING: it requires to be run after the calculation of tf*idf measures
    """
    doc_dict_final = {}

    for wordnum in tf_idf_dict.keys():
        word_dict = tf_idf_dict.get(wordnum)
        tf_idf = word_dict.get(docnum, -1)

        if tf_idf >= 0:
            doc_dict_final[wordnum] = tf_idf

    return doc_dict_final


def euclidean_norm(words_doc_dict):
    """

    """
    sum = 0

    for wordnum in words_doc_dict:
        sum += words_doc_dict[wordnum] * words_doc_dict[wordnum]

    return sqrt(sum)


def cosine_similarity(words_doc1_dict, words_doc2_dict):
    """

    """
    words_doc1_set = set(words_doc1_dict.keys())
    words_doc2_set = set(words_doc2_dict.keys())
    words_intersection = words_doc1_set & words_doc2_set  # '&' operator is used for set intersection

    sum = 0
    for wordnum in words_intersection:
        sum += words_doc1_dict[wordnum] * words_doc2_dict[wordnum]

    norm1 = euclidean_norm(words_doc1_dict)
    norm2 = euclidean_norm(words_doc2_dict)

    cosine_similarity = sum / (norm1 * norm2)

    return cosine_similarity


def calculate_docs_similarity(docname1, docname2, name_num_dict, tf_idf_dict):
    """

    """
    docnum1 = ld.get_docnum_from_name(docname1, name_num_dict)
    docnum2 = ld.get_docnum_from_name(docname2, name_num_dict)

    words_doc1_dict = create_doc_vector_dict(docnum1, tf_idf_dict)
    words_doc2_dict = create_doc_vector_dict(docnum2, tf_idf_dict)

    docs_similarity = cosine_similarity(words_doc1_dict, words_doc2_dict)

    return docs_similarity


if __name__ == '__main__':
    pass