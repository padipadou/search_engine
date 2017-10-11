import time
import memory_profiler
#import resource
import matplotlib.pyplot as plt
import core_functions.load_data as ld
import core_functions.index_data as id
import core_functions.tf_idf as ti
import core_functions.similar_docs as sd
import core_functions.clustering.cluster_data as cl_cl
import core_functions.bm25 as bm25
from core_functions import Const



def main():
    # *------------------------------------------*
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = \
        ld.load_data_dict(Const.DIRECTORY_NAME)
    stopwords = ld.load_stopwords_set()

    # *------------------------------------------*
    print("Creating index...")
    index_dict, word_num_dict, num_word_dict, infos_doc_dict = \
        id.create_index_dict(data_dict, stopwords)

    # *------------------------------------------*
    print("Calculating tf * idf...")
    tf_idf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)

    # *------------------------------------------*
    # print("Calculating similarity between documents...")
    # docname1 = "texte.95-1.txt"
    # docname2 = "texte.95-60.txt"
    # cosine_similarity = \
    #     sd.calculate_docs_similarity(docname1, docname2, name_num_dict, tf_idf_dict)

    # *------------------------------------------*
    print("Clustering...")
    nb_clusters = 31
    docnums_vectors_dict, ward_criteria_list = \
        cl_cl.hca_loop(tf_idf_dict, nb_clusters = nb_clusters)

    print("\tclusters sizes:")
    for docnums_key, vector_value in docnums_vectors_dict.items():
        print("\t", len(docnums_key), '\t document(s):\t', list(docnums_key))
        for i in list(docnums_key):
            print(num_name_dict[i])
        # for wordnum_key, tf_idf_avg_value in vector_value.items():
        #     print(wordnum_key, "\t", num_word_dict[wordnum_key]," : ", tf_idf_avg_value)

    # X = [x for x in range(Const.CORPUS_SIZE, nb_clusters, -1)]
    X = [x for x in range(nb_clusters, Const.CORPUS_SIZE)]
    Y = ward_criteria_list[1:]

    plt.plot(X,Y,'o')
    plt.show()

    # user_query = inpput("whats is your query ?")
    # query_test = "que mangent les hiboux ?"
    # bm25.bm25_function(query_test, stopwords)
    # print(num_name_dict[9])

if __name__ == '__main__':

    t_start = time.time()

    main()

    t_end = time.time()

    print("Temps d'execution = {} seconde(s)\n".format(t_end - t_start))

    #print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)