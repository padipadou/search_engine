import time

import core_functions.load_data as ld
import core_functions.index_data as id
import core_functions.tf_idf as ti
import core_functions.similar_docs as sd
import core_functions.clustering as cl
import core_functions.bm25 as bm25
from core_functions import Const
import matplotlib.pyplot as plt




def main():
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = ld.load_data_dict()
    # data_dict, name_num_dict, num_name_dict = ld.load_data_dict(directory = 'tests/text_to_test/cluster_test')
    stopwords = ld.load_stopwords_set()

    print("Creating index...")
    index_dict, word_num_dict, num_word_dict, infos_doc_dict = \
        id.create_index_dict(data_dict, stopwords)

    # print(index_dict)

    print("Calculating tf * idf...")
    tf_idf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)

    # print(tf_idf_dict)

    # print("Calculating similarity between documents...")
    # docname1 = "texte.95-1.txt"
    # docname2 = "texte.95-60.txt"
    # cosine_similarity = \
    #     sd.calculate_docs_similarity(docname1, docname2, name_num_dict, tf_idf_dict)

    # print(cosine_similarity)

    # print("Clustering...")
    docnums_vectors_dict = cl.hca_loop(tf_idf_dict, nb_clusters = 20)
    docnums_vectors_dict_all = cl.hca_loop(tf_idf_dict, nb_clusters=1)
    # print(docnums_vectors_dict)
    avg_vectors_dict = cl.avg_vectors_dict(docnums_vectors_dict)
    avg_vectors_dict_all = cl.avg_vectors_dict(docnums_vectors_dict_all)


    for valeur in avg_vectors_dict_all.values():
        centreOfGravityDict=valeur

    all_vectors_dict=cl.init_docnums_vectors_dict(tf_idf_dict)

    Itot=cl.compute_Total_Inertia(centreOfGravityDict, all_vectors_dict)
    Iinter=cl.compute_Interclass_Inertia(centreOfGravityDict,avg_vectors_dict)
    Iintra=cl.compute_Intraclass_Inertia(avg_vectors_dict,all_vectors_dict)
    print("Itot="+str(Itot))
    print("Iinter="+str(Iinter))
    print("Iintra="+str(Iintra))

    print("addition Iinter+Iintra=" +(str(Iinter+Iintra)))

    #
    print("\tclusters sizes:")
    for docnums_key, vector_value in avg_vectors_dict.items():
        print("\t", len(docnums_key), '\t document(s):\t', list(docnums_key))
        #for i in list(docnums_key):
            #print(num_name_dict[i])
        #for wordnum_key, tf_idf_avg_value in vector_value.items():
            #print(wordnum_key, "\t", num_word_dict[wordnum_key]," : ", tf_idf_avg_value)


    #plt.plot(X,Y,'o')

    #user_query = inpput("whats is your query ?")
    #query_test = "que mangent les hiboux ?"
    #bm25.bm25_function(query_test, stopwords)
    #print(num_name_dict[9])

if __name__ == '__main__':

    t_start = time.time()

    main()

    t_end = time.time()

    print("Temps d'execution = {} seconde(s)\n".format(t_end - t_start))
