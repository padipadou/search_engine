import libs.kea as kea
import Stemmer as pystemmer
import tqdm as tq
from core_functions import Const


def create_index_dict(datadict, stopwords):
    """
    :param datadict: dict with docnum as key, content of doc as value
    :param stopwords: set of stopwords
    :return:
    index_dict: dict with wordnum as key, dict as value (dict with docnum as key, list of positions OR a count per doc as value)
    word_num_dict: dict with normalized word as key, wordnum as value
    num_word_dict: dict with wordnum  as key, normalized word as value
    infos_doc_dict: dict with docnum  as key, list as value (per doc; list[0]: total nb of words, list[1]: term frequency max)
    """

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

    for page_number in tq.tqdm(datadict.keys()):
        word_position = 0
        term_frequency_max = 0
        content_page = datadict[page_number].split('\n')

        for line in content_page:
            # faster to do it line by line than page by page
            words_line = tokenizer.tokenize(line)

            for word in words_line:

                if word not in stopwords:
                    word_position += 1
                    if Const.STEMMER == True:
                        wordstem = stemmer.stemWord(word).lower()
                    else:
                        wordstem = word

                    word_num = word_num_dict.get(wordstem, -1)

                    # word NOT YET in the index, word NOT YET in the page
                    if word_num < 0:
                        word_num_dict[wordstem] = word_count
                        num_word_dict[word_count] = wordstem
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
                        raise Exception('Issue with word: "{}" \n\tin the page {} \n\tat the position {}'.format(wordstem, page_number, word_position))

        # to get some infos about corpus
        infos_doc_dict[page_number] = []
        # total nb of words
        infos_doc_dict[page_number].append(word_position)
        # term frequency max
        infos_doc_dict[page_number].append(term_frequency_max)

    # BEWARE OF DIFFICULTY WITH BLOC INDEXING /!\/!\/!\ (need to be true for more than one bloc)
    # to get some infos about corpus
    Ndocs_for_a_word_max = Const.NDOCS_FOR_A_WORD_MAX
    for word_occ_dict in index_dict.values():
        Ndocs_for_a_word = len(word_occ_dict)
        if  Ndocs_for_a_word > Ndocs_for_a_word_max:
            Ndocs_for_a_word_max = Ndocs_for_a_word
    Const.NDOCS_FOR_A_WORD_MAX = Ndocs_for_a_word_max

    return index_dict, word_num_dict, num_word_dict, infos_doc_dict


if __name__ == '__main__':
    pass