import core_functions.index_data as id
import core_functions.load_data as ld
import core_functions.similar_docs as sd
import time

def main():
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = ld.load_data_dict()
    stopwords = ld.load_stopwords_set()

    print("Creating index...")
    index_dict, word_num_dict, num_word_dict = \
        id.create_index_dict(data_dict, stopwords)

    # print(index_dict)

    print("Calculating tf * idf...")
    tf_idf_dict = \
        sd.calculate_tf_idf_dict(index_dict)

    # print(tf_idf_dict)

    print("Calculating similarity between documents...")
    docname1 = ""
    docname2 = ""
    cosine_similarity = \
        sd.calculate_docs_similarity(docname1, docname2, name_num_dict, tf_idf_dict)

    print(cosine_similarity)

if __name__ == '__main__':

    t_start = time.time()

    main()

    t_end = time.time()

    print("Temps d'execution = {} seconde(s)\n".format(t_end - t_start))
