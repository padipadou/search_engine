class Const:
    def __init__(self):
        pass

    # Variants for Term Frequency Weight
    # binary, raw_count, term_frequency, log_frequency, double_normal_05
    TF_WEIGHT = 'raw_count'

    # Variants for Inverse Document Frequency Weight
    # unary, idf, idf_smooth, idf_max, idf_probalistic, idf_probalistic_05
    IDF_WEIGHT = 'idf'

    # max number of docs for one word, unknown at the beginning
    NB_DOCS_FOR_A_WORD_MAX = 0

    # way to calculate distances in clustering, only 'avg_linkage' for the moment
    DIST_MEASURE_GROUPS = 'avg_linkage'

    # corpus size is unknown at the beginning
    CORPUS_SIZE = None

    # other possibility : 'tests/text_to_test/cluster_test', 'data/lemonde_utf8', 'data/text_10000'
    DIRECTORY_NAME = 'data/text_10000'

    # true or false
    BM_25 = True

    # true or false
    STEMMER = True

    # true or false -> false allows less memory usage (instead of a position list, only one int)
    POSITIONS_LIST = False

    # size max in Mo for datablocs at the beginning
    MEMORY_SIZE = 200

    # size for one data batch (number of docs)
    MINIBATCH_SIZE = 1000

