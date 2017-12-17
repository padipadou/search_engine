import src.search_engine.sub_steps.normalization as nrm
import src.search_engine.sub_steps.handle_data as hd
import src.other.memory_usage as mem
import src.other.pickle_usage as pck
from src import Const
import libs.kea as kea

from tqdm import tqdm
import Stemmer as pystemmer
import os
from os import remove


def create_index_dict(datadict):
    """
    :param datadict: dict with docnum as key, content of doc as value
    :param stopwords: set of stopwords
    :return:
    index_dict: dict with wordnum as key, dict as value (dict with docnum as key, list of positions OR a count per doc as value)
    word_num_dict: dict with normalized word as key, wordnum as value
    num_word_dict: dict with wordnum  as key, normalized word as value
    infos_doc_dict: dict with docnum  as key, list as value (per doc; list[0]: total nb of words, list[1]: term frequency max)
    """

    stopwords = hd.load_stopwords_set()

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    # stemmer, from PyStemmer
    if Const.STEMMER is True:
        stemmer = pystemmer.Stemmer('french')

    word_num_dict = {}
    num_word_dict = {}
    index_dict = {}
    infos_doc_dict = {}
    word_count = 0

    for page_number in tqdm(datadict.keys()):
        word_position = 0
        term_frequency_max = 0
        content_page = datadict[page_number].split('\n')

        for line in content_page:
            # faster to do it line by line than page by page
            words_line = tokenizer.tokenize(line)

            for word in words_line:

                norm_word = nrm.normalization(word, stopwords, stemmer)
                if norm_word is not None:

                    word_position += 1
                    word_num = word_num_dict.get(norm_word, -1)

                    # word NOT YET in the index, word NOT YET in the page
                    if word_num < 0:
                        word_num_dict[norm_word] = word_count
                        num_word_dict[word_count] = norm_word
                        if Const.POSITIONS_LIST is True:
                            index_dict[word_count] = {page_number: [word_position]}
                        else:
                            index_dict[word_count] = {page_number: 1}

                        if term_frequency_max < 1: term_frequency_max = 1

                        word_count += 1

                    # word ALREADY in the index, word NOT YET in the page
                    elif word_num >= 0 and page_number not in index_dict[word_num]:
                        if Const.POSITIONS_LIST is True:
                            index_dict[word_num] = {**index_dict[word_num], **{page_number: [word_position]}}
                        else:
                            index_dict[word_num] = {**index_dict[word_num], **{page_number: 1}}

                    # word ALREADY in the index, word ALREADY in the page
                    elif word_num >= 0 and page_number in index_dict[word_num]:
                        if Const.POSITIONS_LIST is True:
                            index_dict[word_num][page_number] += [word_position]
                            if term_frequency_max < len(index_dict[word_num][page_number]):
                                term_frequency_max = len(index_dict[word_num][page_number])
                        else:
                            index_dict[word_num][page_number] += 1
                            if term_frequency_max < index_dict[word_num][page_number]:
                                term_frequency_max = index_dict[word_num][page_number]

                    # ERROR
                    else:
                        raise Exception(
                            'Issue with word: "{}" \n\tin the page {} \n\tat the position {}'.format(norm_word,
                                                                                                     page_number,
                                                                                                     word_position))

        # to get some infos about corpus
        infos_doc_dict[page_number] = []
        # total nb of words
        infos_doc_dict[page_number].append(word_position)
        # term frequency max
        infos_doc_dict[page_number].append(term_frequency_max)

    # BEWARE OF DIFFICULTY WITH BLOC INDEXING /!\/!\/!\ (need to be true for more than one bloc)
    # OK if we have only one process done once
    # to get some infos about corpus
    nb_docs_for_a_word_max = Const.NB_DOCS_FOR_A_WORD_MAX
    for word_occ_dict in index_dict.values():
        nb_docs_for_a_word = len(word_occ_dict)
        if nb_docs_for_a_word > nb_docs_for_a_word_max:
            nb_docs_for_a_word_max = nb_docs_for_a_word
    Const.NB_DOCS_FOR_A_WORD_MAX = nb_docs_for_a_word_max

    return index_dict, word_num_dict, num_word_dict, infos_doc_dict


def bloc_indexing(i_start_doc, bloc_num, nb_total_docs, connection=None):
    """
    * Create a directory for each bloc with a precise memory size
    * Create and store num_name_dict, index_dict, word_num_dict, num_word_dict, infos_doc_dict for one bloc
    :param i_start_doc: first doc to look at in repertory
    :param bloc_num: number to store each bloc amongst others
    :param nb_total_docs: max number of wanted docs
    :param connection: connection for the process (easiest way to handle memory)
    :return: i_doc: number of docs which has been explorated in this part
    """

    i_doc = i_start_doc
    minibatch_size = Const.MINIBATCH_SIZE
    max_memory_usage = Const.MEMORY_SIZE  # in Mo

    num_name_dict = {}
    infos_doc_dict = {}
    index_dict = {}
    word_num_dict = {}
    num_word_dict = {}

    while i_doc < nb_total_docs and mem.memory_usage() < max_memory_usage:
        data_dict, num_name_dict_temp = \
            hd.load_data_dict(Const.DIRECTORY_NAME, minibatch_size, i_doc)

        print("Memory usage", mem.memory_usage(), "Mo")

        i_doc += len(data_dict)

        i_newdoc = len(num_name_dict)
        i_newword = len(word_num_dict)

        # -- num_name_dict --
        for key, value in num_name_dict_temp.items():
            num_name_dict[i_newdoc + key] = value
        del num_name_dict_temp

        # /!\ word_num_dict_temp useless
        index_dict_temp, word_num_dict_temp, num_word_dict_temp, infos_doc_dict_temp = \
            create_index_dict(data_dict)
        del data_dict

        # -- infos_doc_dict --
        for key, value in infos_doc_dict_temp.items():
            infos_doc_dict[i_newdoc + key] = value
        del infos_doc_dict_temp

        # -- index_dict, num_word_dict, word_num_dict --
        for wordnum_key_temp, dict_value_temp in index_dict_temp.items():
            norm_word = num_word_dict_temp[wordnum_key_temp]
            word_num = word_num_dict.get(norm_word, -1)

            # word NOT YET in the global index
            if word_num < 0:
                word_num_dict[norm_word] = i_newword
                num_word_dict[i_newword] = norm_word
                index_dict[i_newword] = {}

                for docnum_key_temp, pos_count_value_temp in dict_value_temp.items():
                    docnum = i_newdoc + docnum_key_temp
                    index_dict[i_newword] = {**index_dict[i_newword], **{docnum: pos_count_value_temp}}
                i_newword += 1

            # word ALREADY in the global index
            else:
                for docnum_key_temp, pos_count_value_temp in dict_value_temp.items():
                    docnum = i_newdoc + docnum_key_temp
                    index_dict[word_num] = {**index_dict[word_num], **{docnum: pos_count_value_temp}}

        del index_dict_temp
        del num_word_dict_temp

    # Storing dictionaries
    try:
        os.mkdir("data/pickle_files/b_{}".format(bloc_num))
    except:
        remove("data/pickle_files/b_{}".format(bloc_num))
        os.mkdir("data/pickle_files/b_{}".format(bloc_num))

    if num_name_dict and infos_doc_dict and index_dict and word_num_dict and num_word_dict:
        path_name = "b_{}/num_name_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, num_name_dict, "")
        del num_name_dict

        path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, index_dict, "")
        del index_dict

        path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, word_num_dict, "")
        del word_num_dict

        path_name = "b_{}/num_word_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, num_word_dict, "")
        del num_word_dict

        path_name = "b_{}/infos_doc_dict_b{}".format(bloc_num, bloc_num)
        pck.pickle_store(path_name, infos_doc_dict, "")
        del infos_doc_dict

    # Return nb_docs done
    if connection:
        connection.send(i_doc)
        connection.close()
    else:
        return i_doc


if __name__ == '__main__':
    pass
