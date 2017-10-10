class Const:
    def __init__(self):
        pass

    # Variants for Term Frequency Weight
    # binary, raw_count, term_frequency, log_frequency, double_normal_05
    TF_WEIGHT = 'raw_count'

    # Variants for Inverse Document Frequency Weight
    # unary, idf, idf_smooth, idf_max, idf_probalistic, idf_probalistic_05
    IDF_WEIGHT = 'idf'

    NDOCS_FOR_A_WORD_MAX = None

    DIST_MEASURE_GROUPS = 'avg_linkage'

    CORPUS_SIZE = None

    # other possibility : 'tests/text_to_test/cluster_test', 'data/lemonde-utf8'
    DIRECTORY_NAME = 'data/lemonde-utf8'

