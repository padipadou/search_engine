import time

import core_functions.load_data as ld
import core_functions.index_data as id
import core_functions.tf_idf as ti
import core_functions.similar_docs as sd
import core_functions.clustering as cl



def main():
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = ld.load_data_dict()
    stopwords = ld.load_stopwords_set()

    print("Creating index...")
    index_dict, word_num_dict, num_word_dict, infos_doc_dict = \
        id.create_index_dict(data_dict, stopwords)

    # print(index_dict)

    print("Calculating tf * idf...")
    tf_idf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)

    print(tf_idf_dict)

    print("Calculating similarity between documents...")
    docname1 = "texte.95-1.txt"
    docname2 = "texte.95-60.txt"
    cosine_similarity = \
        sd.calculate_docs_similarity(docname1, docname2, name_num_dict, tf_idf_dict)

    print(cosine_similarity)

    L,numL= cl.create_List_Vectors_dict(tf_idf_dict)

    numL=cl.HCA_loop(L, numL,5)
    print("groups:")
    print(numL)
    print("clusters number : "+ str(len(numL)))


    print("Clusters sizes:")
    for i in range(len(numL)):
        print(str(i)+": " + str(len(numL[i])))

    #print(sd.calculate_docs_similarity("texte.95-10.txt", "texte.95-11.txt", name_num_dict, tf_idf_dict))

if __name__ == '__main__':

    t_start = time.time()

    main()

    t_end = time.time()

    print("Temps d'execution = {} seconde(s)\n".format(t_end - t_start))
