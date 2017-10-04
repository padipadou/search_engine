import tqdm as tq

def calculate_tf_idf_dict(index_dict):
    """
    Returns a num linked to a name (docname).
    """
    tf_idf_dict = {}

    for word in tq.tqdm(index_dict.keys()):
        word_dict = index_dict.get(word)
        idf = 1/len(word_dict)
        tf_idf_word_dict = {}

        for document in word_dict.keys():
            positions_list = word_dict.get(document)
            tf = len(positions_list)
            tf_idf_word_dict[document] = tf * idf

        tf_idf_dict[word] = tf_idf_word_dict
    return tf_idf_dict


def create_doc_vector_dict():
    """
    Creates and returns a dict linked to a doc with words in it and the tf*idf for each of them.
    WARNING: it requires to be run after the calculation of tf*idf measures
    """


    pass

def cosine_similarity(word_dict1, word_dict2):
    docs_set_1 = set(word_dict1.keys())
    docs_set_2 = set(word_dict2.keys())

    docs_intersection = docs_set_1 & docs_set_2  # '&' operator is used for set intersection

    sum = 0
    for doc in docs_intersection:
        sum += word_dict1[doc] * word_dict2[doc]

    for doc in docs_set_1:
        pass

if __name__ == '__main__':
    pass