import core_functions.load_data as ld
from math import sqrt


def create_doc_vector_dict(docnum, tf_idf_dict):
    """
    Creates and returns a dict linked to only ONE doc with words as keys in it and the tf*idf as values for each of them.
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
    Returns Euclidean norm for any words_doc_dict vector.
    WARNING: the dict must have the correct form
        key: wordnum
        value: tf*idf
    """
    sum = 0

    for wordnum in words_doc_dict:
        sum += words_doc_dict[wordnum] * words_doc_dict[wordnum]

    euclidean_norm = sqrt(sum)

    return euclidean_norm


def calculate_cosine(words_doc1_dict, words_doc2_dict):
    """
    Returns cosine between two vectors, each of them are linked to one document.
    WARNING: the dicts must have the correct form
        key: wordnum
        value: tf*idf
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
    Full function to get similarity between two docs.
    """
    docnum1 = ld.get_docnum_from_name(docname1, name_num_dict)
    docnum2 = ld.get_docnum_from_name(docname2, name_num_dict)

    words_doc1_dict = create_doc_vector_dict(docnum1, tf_idf_dict)
    words_doc2_dict = create_doc_vector_dict(docnum2, tf_idf_dict)

    docs_similarity = calculate_cosine(words_doc1_dict, words_doc2_dict)

    return docs_similarity


if __name__ == '__main__':
    pass