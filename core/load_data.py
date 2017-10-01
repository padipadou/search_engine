import os

def load_data_dict():
    """
    Creates and returns a dict containing file num as key, file content as value.
    """
    dir = '../data/lemonde-utf8'

    data_dict = {}
    for i,filename in enumerate(os.listdir(dir)):
        path = '{}/{}'.format(dir, filename)
        with open(path, 'r') as infile:
            data_dict[i] = infile.read()

    return data_dict

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