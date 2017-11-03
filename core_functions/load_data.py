import os


def load_data_dict(directory, number_files=None, indice_start=0):
    """
    Creates and returns a dict containing file num as key, file content as value.
    Creates and returns a dict containing filename as key, filenum as value.
    Creates and returns a dict containing filenum as key, filename as value.
    """

    data_dict = {}
    name_num_dict = {}
    num_name_dict = {}

    # Initial mode: with 100 docs
    if number_files is None:
        # dir_ = 'data/lemonde-utf8'
        for i, filename in enumerate(os.listdir(directory)):
            path = '{}/{}'.format(directory, filename)
            name_num_dict[filename] = i
            num_name_dict[i] = filename

            with open(path, 'r') as infile:
                data_dict[i] = infile.read()
    # Larger mode: with number_files documents
    else:
        i_global = 0
        file_count = 0
        # dir_ = 'data/text_10000'
        current_path_0 = directory
        for year_dir in os.listdir(current_path_0):
            current_path_1 = current_path_0 + '/' + year_dir
            for month_dir in os.listdir(current_path_1):
                current_path_2 = current_path_1 + '/' + month_dir
                for day_dir in os.listdir(current_path_2):
                    current_path_3 = current_path_2 + '/' + month_dir
                    for filename in os.listdir(current_path_3):
                        file_count += 1
                        # No need to read this file
                        if file_count < indice_start:
                            pass
                        # This file is necessary for this batch
                        elif file_count >= indice_start and i_global < number_files:
                            current_path_4 = current_path_3 + '/' + filename
                            name_num_dict[filename] = i_global
                            num_name_dict[i_global] = filename

                            with open(current_path_4, 'r') as infile:
                                data_dict[i_global] = infile.read()
                            i_global += 1
                        # We have enough files for this batch
                        elif i_global >= number_files:
                            return data_dict, name_num_dict, num_name_dict

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


def load_stopwords_set(path='data/stopwords-fr.txt'):
    """
    Creates and returns a set containing stopwords which are in the file.
    """
    stopwords = []

    with open(path, 'r') as stopwords_file:
        for stopword in stopwords_file:
            stopwords.append(stopword.split()[0])

    return set(stopwords)


if __name__ == '__main__':
    pass