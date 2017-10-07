import core_functions.index_data as id
import load_data_test as ld
import time

def main():
    print("Loading data...")
    data_dict, name_num_dict, num_name_dict = ld.load_data_dict()
    stopwords = ld.load_stopwords_set()

    print("Creating index...")
    index_dict, word_num_dict, num_word_dict = \
        id.create_index_dict(data_dict, stopwords)

    print(index_dict)


if __name__ == '__main__':
    time0 = time.time()

    main()

    duration = time.time() - time0

    print("Temps d'execution = {} seconde(s)\n".format(duration))
