import os


def load_data_dict(directory):
    """
    Creates and returns a dict containing file num as key, file content as value.
    Creates and returns a dict containing filename as key, filenum as value.
    Creates and returns a dict containing filenum as key, filename as value.
    """

    data_dict = {}
    name_num_dict = {}
    num_name_dict = {}
    for i,filename in enumerate(os.listdir(directory)):
        path = '{}/{}'.format(directory, filename)
        name_num_dict[filename] = i
        num_name_dict[i] = filename

        with open(path, 'r') as infile:
            data_dict[i] = infile.read()

    return data_dict, name_num_dict, num_name_dict


def get_docnum_from_name(name, name_num_dict):
    """
    Returns a num linked to a name (docname).
    """
    docnum = name_num_dict.get(name,-1)

    if docnum >= 0:
        return docnum
    # ERROR
    else:
        raise Exception("'{}' is not a document !")


def load_stopwords_set():
    """
    Creates and returns a set containing stopwords which are in the file.
    """
    stopwords = []
    path = 'data/stopwords-fr.txt'

    with open(path, 'r') as stopwords_file:
        for stopword in stopwords_file:
            stopwords.append(stopword.split()[0])

    return set(stopwords)


if __name__ == '__main__':
    pass