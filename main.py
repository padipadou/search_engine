import os
import time
from tqdm import tqdm

from memory_profiler import profile

import core_functions.bm25 as bm25
import core_functions.clustering.cluster_data as cl_cl
import core_functions.handle_data as hd
import core_functions.index_data as idxd
import core_functions.pickle_usage as pck
import core_functions.tf_idf as ti
from core_functions import Const
import core_functions.bloc_working as bw


#@profile
def index_creation_part():
    # *------------------------------------------*
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = \
        hd.load_data_dict(Const.DIRECTORY_NAME)
    stopwords = hd.load_stopwords_set()

    # *------------------------------------------*
    print("Creating index...")
    index_dict, word_num_dict, num_word_dict, infos_doc_dict = \
        idxd.create_index_dict(data_dict, stopwords)

    # *------------------------------------------*
    print("Calculating tf * idf...")
    tf_idf_dict, tf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)

    # *------------------------------------------*
    print("Clustering...")
    nb_clusters = 31
    docnums_vectors_dict, ward_criteria_list = \
        cl_cl.hca_loop(tf_idf_dict, nb_clusters=nb_clusters)

    del data_dict
    del name_num_dict
    del ward_criteria_list

    pck.pickle_store("num_name_dict", num_name_dict, "")
    pck.pickle_store("index_dict", index_dict, "")
    pck.pickle_store("num_word_dict", num_word_dict, "")
    pck.pickle_store("docnums_vectors_dict", docnums_vectors_dict, "")
    pck.pickle_store("infos_doc_dict", infos_doc_dict, "")
    pck.pickle_store("tf_dict", tf_dict, "")
    pck.pickle_store("word_num_dict", word_num_dict, "")
    pck.pickle_store("tf_idf_dict", tf_idf_dict, "")

    del word_num_dict
    del tf_idf_dict
    del num_name_dict
    del index_dict
    del num_word_dict
    del docnums_vectors_dict
    del infos_doc_dict
    del tf_dict


def after_index_creation_part():
    num_name_dict = pck.pickle_load("num_name_dict", "")
    index_dict = pck.pickle_load("index_dict", "")
    num_word_dict = pck.pickle_load("num_word_dict", "")
    word_num_dict = pck.pickle_load("word_num_dict", "")
    tf_idf_dict = pck.pickle_load("tf_idf_dict", "")
    docnums_vectors_dict = pck.pickle_load("docnums_vectors_dict", "")
    infos_doc_dict = pck.pickle_load("infos_doc_dict", "")
    tf_dict = pck.pickle_load("tf_dict", "")

    # print("\tclusters sizes:")
    # for docnums_key, vector_value in docnums_vectors_dict.items():
    #     print("\t", len(docnums_key), '\t document(s):\t', list(docnums_key))
        # for i in list(docnums_key):
        #     print(num_name_dict[i])
        # for wordnum_key, tf_idf_avg_value in vector_value.items():
        #     print(wordnum_key, "\t", num_word_dict[wordnum_key]," : ", tf_idf_avg_value)

    # user_query = inpput("whats is your query ?")
    query_test = "israël jérusalem"
    stopwords = hd.load_stopwords_set()

    docnum_score_sum_dict = \
        bm25.bm25_function(query_test, stopwords, word_num_dict, tf_idf_dict, tf_dict, infos_doc_dict)

    for key, value in sorted(docnum_score_sum_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print("{}: \t{}".format(num_name_dict[key], value))


# @profile
def main():
    # index_creation_part()
    # after_index_creation_part()

    # NEED MULTIPROCESSING
    bloc_size = 100
    total_nb_blocs = 4  # 2 power something
    for blocnum in range(0, total_nb_blocs, 1):
        print(blocnum+1, "/", total_nb_blocs, "...")
        bw.bloc_indexing(blocnum, bloc_size)

    print("Merging...")

    gap = 1
    while gap < total_nb_blocs:
        gap *= 2
        for blocnum in range(0, total_nb_blocs, gap):
            neighboor_blocnum = int(blocnum + gap/2)
            bw.bloc_merging(blocnum, neighboor_blocnum, bloc_size)


if __name__ == '__main__':

    t_start = time.time()

    main()

    t_end = time.time()

    print("Running time = {} second(s)\n".format(t_end - t_start))

