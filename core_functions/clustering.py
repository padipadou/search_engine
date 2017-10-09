import core_functions.similar_docs as sd
from core_functions import Const


def init_docnums_vectors_dict(tf_idf_dict):
    """
    Creates and returns a dict with set of ONE docnum as keys, and tf_idf_dict vector linked ONLY to this doc as value.
    WARNING: it requires to be run after the calculation of tf*idf measures
    """
    docnums_vectors_lists_dict = {}

    for docnum in range(Const.CORPUS_SIZE):
        docnums_set = frozenset([docnum])
        doc_vectors_list = [sd.create_doc_vector_dict(docnum, tf_idf_dict)]

        docnums_vectors_lists_dict[docnums_set] = doc_vectors_list

    return docnums_vectors_lists_dict


def average_linkage(dv_list_i, dv_list_j):
    """
    average linkage with cosine between two vectors
    :param dv_list_i:
    :param dv_list_j:
    :return:
    """
    similarity = 0

    for vect_i in dv_list_i:
        for vect_j in dv_list_j:
            similarity += sd.calculate_cosine(vect_i, vect_j)

    similarity *= 1 / (len(dv_list_i) * len(dv_list_j))

    return similarity


def merge_closest_elements(docnums_vectors_dict):
    """
    Computes the two nearest elements of the docnums_vectors_dict (values from this dict)
    Updates docnums_vectors_dict by merging the nearest elements
    """
    similarity_max = 0
    already_seen_keys = set()
    keys_to_see_global = docnums_vectors_dict.keys()

    # Looking for the 2 closest doc_vectors
    for dv_key_i in keys_to_see_global:
        already_seen_keys.add(dv_key_i)
        keys_to_see = set(keys_to_see_global).difference(already_seen_keys)

        for dv_key_j in keys_to_see:
            dv_list_i = docnums_vectors_dict[dv_key_i]
            dv_list_j = docnums_vectors_dict[dv_key_j]

            if len(dv_list_i) == 1 and len(dv_list_j) == 1:
                vect_i = dv_list_i[0]
                vect_j = dv_list_j[0]

                current_similarity = sd.calculate_cosine(vect_i, vect_j)

            #If we compare 2 groups of texts - Average linkage -----------we can use another method
            else:
                if Const.DIST_MEASURE_GROUPS == 'avg_linkage':
                    current_similarity = average_linkage(dv_list_i, dv_list_j)
                else:
                    raise "Error with measure."

            if current_similarity > similarity_max:
                similarity_max = current_similarity

                vectors_sim_max_i = dv_list_i
                vectors_sim_max_j = dv_list_j
                docnums_sim_max_i = dv_key_i
                docnums_sim_max_j = dv_key_j

    # Merging part
    try: #NEED TO BE CHANGED
        docnums_sim_max = frozenset(list(docnums_sim_max_i) + list(docnums_sim_max_j))
    except:
        try:
            docnums_sim_max = frozenset([docnums_sim_max_i] + list(docnums_sim_max_j))
        except:
            try:
                docnums_sim_max = frozenset(list(docnums_sim_max_i) + [docnums_sim_max_j])
            except:
                docnums_sim_max = frozenset([docnums_sim_max_i] + [docnums_sim_max_j])

    vectors_sim_max = vectors_sim_max_i + vectors_sim_max_j

    docnums_vectors_dict[docnums_sim_max] = vectors_sim_max

    del docnums_vectors_dict[docnums_sim_max_i]
    del docnums_vectors_dict[docnums_sim_max_j]

    return docnums_vectors_dict


def hca_loop(tf_idf_dict, nb_clusters):
    """
    Returns a dict with groups (sets) of docnum (clusters) as keys and tf*idf vectors list as values.
    Clusters have been made using the hierarchical cluster analysis.
    """

    docnums_vectors_dict = init_docnums_vectors_dict(tf_idf_dict)

    if nb_clusters >= len(docnums_vectors_dict):
        raise Exception('"nb_clusters" must be inferior than the total number of files.')

    else:
        while len(docnums_vectors_dict) > nb_clusters:
            docnums_vectors_dict = merge_closest_elements(docnums_vectors_dict)

        return docnums_vectors_dict


def average_vector(vectors_dict_list):
    """
    return a vector dict which the average of the vectorlist.
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
    Returns a dict with average vector dict for each group of vectors previously made by clustering
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

