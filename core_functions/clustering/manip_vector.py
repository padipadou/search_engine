
def average_vector(vectors_dict_list):
    """
    return a VECTOR dict with the average of the vectorlist values as values, and the exact same keys.
    :param vectors_list:
    :return:
    """
    nb_vectors = len(vectors_dict_list)
    avg_dict = {}

    for vector in vectors_dict_list:
        for wordnum_key, tf_idf_value in vector.items():
            if wordnum_key not in avg_dict.keys():
                avg_dict[wordnum_key] = tf_idf_value
            else:
                avg_dict[wordnum_key] += tf_idf_value

    for wordnum_key in avg_dict.keys():
        avg_dict[wordnum_key] *= 1 / nb_vectors

    return avg_dict


def avg_vectors_dict(docnums_vectors_dict):
    """
    Returns a DICT with average vector dict for each group of vectors previously made by clustering
    :param docnums_vectors_dict:
    :return:
    """
    docnums_vectors_avg_dict = {}
    for docnums_key, vectors_value in docnums_vectors_dict.items():
        if len(docnums_key) > 1:
            avg_vector = average_vector(vectors_value)
        else:
            avg_vector = vectors_value

        docnums_vectors_avg_dict[docnums_key] = avg_vector

    return docnums_vectors_avg_dict


if __name__ == '__main__':
    pass