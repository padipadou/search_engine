import core_functions.similar_docs as sd


def init_docnums_vectors_dict(tf_idf_dict):
    """
    Creates and returns a list of dicts with words as keys and the tf*idf as values for each of them.
    Also returns a list of document numbers : the element i in vectors_list refers to the doc number  docnum_list[i]
    WARNING: it requires to be run after the calculation of tf*idf measures

    Creates and returns a dict with tuple of ONE docnum as key, and tf_idf_dict linked ONLY to this doc as value.
    WARNING: it requires to be run after the calculation of tf*idf measures
    """
    # vectors_list = []
    # docnum_list = []
    #
    # for docnum in range(107): #107 has to be changed
    #     vectors_list.append([sd.create_doc_vector_dict(docnum, tf_idf_dict)])
    #     docnum_list.append([docnum])
    #
    # return vectors_list, docnum_list

    docnums_vectors_lists_dict = {}

    for docnum in range(107): #107 has to be changed
        docnums_set = frozenset([docnum])
        doc_vectors_list = [sd.create_doc_vector_dict(docnum, tf_idf_dict)]

        docnums_vectors_lists_dict[docnums_set] = doc_vectors_list

    return docnums_vectors_lists_dict


def average_linkage(dv_list_i, dv_list_j):
    similarity = 0

    for vect_i in dv_list_i:
        for vect_j in dv_list_j:
            similarity += sd.calculate_cosine(vect_i, vect_j)

    similarity *= 1 / (len(dv_list_i) * len(dv_list_j))

    return similarity


def merge_closest_elements(docnums_vectors_dict):
    """
    Computes the two nearest elements of the vectorsList
    Updates vectorsList and numberList by melting the nearest elements
    """
    similarity_max = 0
    already_seen_keys = set()

    keys_to_see_global = docnums_vectors_dict.keys()

    # Looking for the 2 closest doc_vectors
    for dv_key_i in keys_to_see_global:
        already_seen_keys.add(dv_key_i)
        keys_to_see = set(keys_to_see_global).difference(already_seen_keys)

        for dv_key_j in keys_to_see:
            current_similarity = 0

            #If we compare two texts
            dv_list_i = docnums_vectors_dict[dv_key_i]
            dv_list_j = docnums_vectors_dict[dv_key_j]

            if len(dv_list_i) == 1 and len(dv_list_j) == 1:
                vect_i = dv_list_i[0]
                vect_j = dv_list_j[0]

                current_similarity = \
                    sd.calculate_cosine(vect_i, vect_j)

            #If we compare 2 groups of texts - Average linkage -----------we can use another method
            else:
                current_similarity = average_linkage(dv_list_i, dv_list_j)

            if current_similarity > similarity_max:
                similarity_max = current_similarity

                vectors_sim_max_i = dv_list_i
                vectors_sim_max_j = dv_list_j
                docnums_sim_max_i = dv_key_i
                docnums_sim_max_j = dv_key_j

                #id1=vectors_list.index(List_i)
                #id2=vectors_list.index(List_j)

    # Merge
    try:
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
    Returns a list composed of nbClusters lists of documents by using the hierarchical cluster analysis
    """

    docnums_vectors_dict = init_docnums_vectors_dict(tf_idf_dict)

    if nb_clusters >= len(docnums_vectors_dict):
        raise Exception('"nb_clusters" must be inferior than the total number of files.')

    else:
        while len(docnums_vectors_dict) > nb_clusters:
            docnums_vectors_dict = merge_closest_elements(docnums_vectors_dict)

        return docnums_vectors_dict

if __name__ == '__main__':
    pass

