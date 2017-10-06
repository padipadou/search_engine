class Const:
    def __init__(self):
        pass

    # Variants for Term Frequency Weight
    # binary, raw_count, term_frequency, log_frequency, double_normal_05
    TF_WEIGHT = 'raw_count'

    # Variants for Inverse Document Frequency Weight
    # unary, idf, idf_smooth, idf_max, idf_probalistic
    IDF_WEIGHT = 'idf'
