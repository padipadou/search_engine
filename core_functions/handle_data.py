import os


def load_data_dict(directory, nb_files_needed=None, indice_start=0):
    """
    :param directory: root to read files
    :param nb_files_needed: number of files that you need
    :param indice_start: number of the first file that you need
    :return:
    data_dict: dict with docnum as key, content of doc as value
    num_name_dict: dict with docnum as key, doc name  as value
    """

    data_dict = {}
    num_name_dict = {}

    # Initial mode: with 100 docs
    if nb_files_needed is None:
        # dir_ = 'data/lemonde_utf8'
        for i, filename in enumerate(os.listdir(directory)):
            path = '{}/{}'.format(directory, filename)
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
            if year_dir == ".DS_Store":
                pass
            current_path_1 = current_path_0 + '/' + year_dir
            for month_dir in os.listdir(current_path_1):
                if month_dir == ".DS_Store":
                    pass
                current_path_2 = current_path_1 + '/' + month_dir
                for day_dir in os.listdir(current_path_2):
                    if day_dir == ".DS_Store":
                        pass
                    current_path_3 = current_path_2 + '/' + day_dir
                    for filename in os.listdir(current_path_3):
                        if filename == ".DS_Store":
                            pass
                        file_count += 1
                        # No need to read this file
                        if file_count < indice_start:
                            pass

                        # This file is necessary for this batch (if it exists)
                        elif file_count >= indice_start and i_global < nb_files_needed:
                            current_path_4 = current_path_3 + '/' + filename
                            num_name_dict[i_global] = filename

                            try:
                                with open(current_path_4, 'r', encoding="utf-8") as infile:
                                    data_dict[i_global] = infile.read()
                                i_global += 1
                            except:
                                print("Not enough files ! Only {} here.".format(i_global))
                                return data_dict, num_name_dict

                        # We have enough files for this batch
                        elif i_global >= nb_files_needed:
                            return data_dict, num_name_dict

    return data_dict, num_name_dict


def load_stopwords_set(path='data/stopwords-fr.txt'):
    """
    Creates and returns a set containing stopwords which are in the file.
    """
    stopwords = []

    with open(path, 'r', encoding="utf-8") as stopwords_file:
        for stopword in stopwords_file:
            stopwords.append(stopword.split()[0])

    return set(stopwords)


if __name__ == '__main__':
    pass
