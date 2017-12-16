import os

def load_data_dict():
    """
    Creates and returns a dict containing file num as key, file content as value.
    Creates and returns a dict containing filename as key, filenum as value.
    Creates and returns a dict containing filenum as key, filename as value.
    """
    dir = '../tests/text_to_test'

    data_dict = {}
    name_num_dict = {}
    num_name_dict = {}
    for i,filename in enumerate(os.listdir(dir)):
        path = '{}/{}'.format(dir, filename)
        name_num_dict[filename] = i
        num_name_dict[i] = filename

        with open(path, 'r') as infile:
            data_dict[i] = infile.read()

    return data_dict, name_num_dict, num_name_dict

def load_hiboudata_dict():
    """
    Creates and returns a dict containing file num as key, file content as value.
    Creates and returns a dict containing filename as key, filenum as value.
    Creates and returns a dict containing filenum as key, filename as value.
    """
    dir = '../tests/text_to_test'

    data_dict = {}
    name_num_dict = {}
    num_name_dict = {}
    filename = 'hibou.txt'
    i = 0

    # exact same running as normal function
    path = '{}/{}'.format(dir, filename)
    name_num_dict[filename] = i
    num_name_dict[i] = filename

    with open(path, 'r') as infile:
        data_dict[i] = infile.read()

    return data_dict, name_num_dict, num_name_dict

def load_stopwords_set():
    """
    Creates and returns a set containing stopwords which are in the file.
    """
    stopwords = []
    path = '../data/stopwords-fr.txt'

    with open(path, 'r') as stopwords_file:
        for stopword in stopwords_file:
            stopwords.append(stopword.split()[0])

    return set(stopwords)


if __name__ == '__main__':
    import src.search_engine.index_data as id
    import tests.load_data_test as ldtest

    data_dict, name_num_dict, num_name_dict = ldtest.load_hiboudata_dict()
    stopwords = ldtest.load_stopwords_set()
    index_dict, word_num_dict, num_word_dict, info_doc_dict = id.create_index_dict(data_dict, stopwords)

    print(index_dict)
    print(num_word_dict)
    print(word_num_dict["hibou"])

    pass