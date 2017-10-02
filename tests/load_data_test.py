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
    pass