import time
from memory_profiler import profile
import matplotlib.pyplot as plt
import core_functions.load_data as ld
import core_functions.index_data as id
import core_functions.tf_idf as ti
import core_functions.similar_docs as sd
import core_functions.clustering.cluster_data as cl_cl
import core_functions.bm25 as bm25
from core_functions import Const
import pickle

DIRECTORY_NAME = "../data/lemonde-utf8"


def pickle_store(object_name, value, prefix_path="../"):
    file_path = "{}data/{}.pickle".format(prefix_path, object_name)

    with open(file_path, 'wb') as file_object:
        pickle.dump(value, file_object, pickle.HIGHEST_PROTOCOL)


def store_part():
    # *------------------------------------------*
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = \
        ld.load_data_dict(DIRECTORY_NAME)
    stopwords = ld.load_stopwords_set('../data/stopwords-fr.txt')

    # *------------------------------------------*
    print("Creating index...")
    index_dict, word_num_dict, num_word_dict, infos_doc_dict = \
        id.create_index_dict(data_dict, stopwords)

    # *------------------------------------------*
    print("Calculating tf * idf...")
    tf_idf_dict, tf_dict = \
        ti.calculate_tf_idf_dict(index_dict, infos_doc_dict)
    docnums_vectors_dict = \
        cl_cl.init_docnums_vectors_dict(tf_idf_dict,"normal")


    pickle_store("num_name_dict", num_name_dict)
    pickle_store("index_dict", index_dict)
    pickle_store("num_word_dict", num_word_dict)
    pickle_store("docnums_vectors_dict", docnums_vectors_dict)

    del num_name_dict
    del index_dict
    del num_word_dict
    del docnums_vectors_dict

    #time.sleep(1)


def pickle_load(object_name, prefix_path="../"):
    file_path = "{}data/{}.pickle".format(prefix_path, object_name)

    with open(file_path, 'rb') as file_object:
        return pickle.load(file_object)


def restore_part():

    num_name_dict = pickle_load("num_name_dict")
    index_dict = pickle_load("index_dict")
    num_word_dict = pickle_load("num_word_dict")
    docnums_vectors_dict = pickle_load("docnums_vectors_dict")

    docnum = 2
    print("Doc :\t", num_name_dict[docnum], "\n")

    dict = docnums_vectors_dict[docnum]
    for key, value in sorted(dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print("{}: \t{}".format(num_word_dict[key], value))


#@profile
def main():
    restore_part()


if __name__ == "__main__":

    t_start = time.time()

    main()

    t_end = time.time()

    print("Temps d'execution = {} seconde(s)\n".format(t_end - t_start))