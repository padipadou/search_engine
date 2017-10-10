import core_functions.similar_docs as sd
import core_functions.clustering.inertia as cl_in
import core_functions.clustering.manip_vector as cl_mv
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


def init_docnums_vectors_dict_one_group(tf_idf_dict):
    """
    Creates and returns a dict with ONE set of ALL docnum as keys, and tf_idf_dict vector linked to these docs as value.
    WARNING: it requires to be run after the calculation of tf*idf measures
    ONLY ONE GROUP
    """
    docnums_vectors_lists_dict = {}

    docnums_set = frozenset([docnum for docnum in range(Const.CORPUS_SIZE)])
    doc_vectors_list = [sd.create_doc_vector_dict(docnum, tf_idf_dict) for docnum in range(Const.CORPUS_SIZE)]

    docnums_vectors_lists_dict[docnums_set] = doc_vectors_list

    return docnums_vectors_lists_dict


def average_linkage(dv_list_i, dv_list_j):
    """
    average linkage with cosine between two vectors
    WARNING: it is a similarity not a distance
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

    # -- Looking for the 2 closest doc_vectors --
    for dv_key_i in keys_to_see_global:
        already_seen_keys.add(dv_key_i)
        keys_to_see = set(keys_to_see_global).difference(already_seen_keys)

        for dv_key_j in keys_to_see:
            dv_list_i = docnums_vectors_dict[dv_key_i]
            dv_list_j = docnums_vectors_dict[dv_key_j]

            # Comparison between 2 ONE-vector's classes
            if len(dv_list_i) == 1 and len(dv_list_j) == 1:
                vect_i = dv_list_i[0]
                vect_j = dv_list_j[0]

                current_similarity = sd.calculate_cosine(vect_i, vect_j)

            # Comparison between 2 groups of SEVERAL vectors
            # (at least one group with several vectors)
            else:
                if Const.DIST_MEASURE_GROUPS == 'avg_linkage':
                    current_similarity = average_linkage(dv_list_i, dv_list_j)
                else:
                    raise Exception("Error with measure.")

            # Is it the closest relation ?
            if current_similarity > similarity_max:
                similarity_max = current_similarity

                vectors_sim_max_i = dv_list_i
                vectors_sim_max_j = dv_list_j
                docnums_sim_max_i = dv_key_i
                docnums_sim_max_j = dv_key_j

    # -- Merging part --
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

    # New class with previous classes merged
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

    if nb_clusters > len(docnums_vectors_dict):
        raise Exception('"nb_clusters" must be inferior than the total number of files.')

    else:
        ward_criteria_list = []

        # Creation of gravity_center_dict
        docnums_vectors_dict_1g = init_docnums_vectors_dict_one_group(tf_idf_dict)
        avg_vectors_dict = cl_mv.avg_vectors_dict(docnums_vectors_dict_1g)
        for value in avg_vectors_dict.values():
            gravity_center_dict = value

        # First Ward criteria
        Itot = cl_in.compute_Total_Inertia(gravity_center_dict, docnums_vectors_dict)
        Iinter = cl_in.compute_Interclass_Inertia(gravity_center_dict, avg_vectors_dict)
        ward_criteria = Iinter / Itot
        ward_criteria_list.append(ward_criteria)

        while len(docnums_vectors_dict) > nb_clusters:
            docnums_vectors_dict = merge_closest_elements(docnums_vectors_dict)

            # Calculation avg on groups to get distance between groups with Iinter
            avg_vectors_dict = cl_mv.avg_vectors_dict(docnums_vectors_dict)
            Iinter = cl_in.compute_Interclass_Inertia(gravity_center_dict, avg_vectors_dict)
            ward_criteria = Iinter / Itot
            ward_criteria_list.append(ward_criteria)

        return docnums_vectors_dict, ward_criteria_list


if __name__ == '__main__':
    pass

