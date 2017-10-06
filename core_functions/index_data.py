import libs.kea as kea
import Stemmer as pystemmer
import tqdm as tq

def create_index_dict(datadict, stopwords):
    """
    Creates and returns the positional index for all the files in datadict.
    Creates and returns a dict containing a word as key, wordnum as value for all the words in datadict.
    Creates and returns a dict containing a wordnum as key, word as value for all the words in datadict.
    Creates and returns a dict containing a docnum as key, number of interesting words as value for all the files in datadict.
    """
    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    # stemmer, from PyStemmer
    stemmer = pystemmer.Stemmer('french')

    word_num_dict = {}
    num_word_dict = {}
    index_dict = {}
    infos_doc_dict = {}
    word_count = 0

    for page_number in tq.tqdm(datadict.keys()):
        word_position = 0
        term_frequency_max = 0
        content_page = datadict[page_number].lower().split('\n')

        for line in content_page:
            # faster to do it line by line than page by page
            words_line = tokenizer.tokenize(line)

            for word in words_line:

                if word not in stopwords:
                    word_position += 1
                    wordstem = stemmer.stemWord(word)

                    word_num = word_num_dict.get(wordstem,-1)

                    # word NOT YET in the index, word NOT YET in the page
                    if word_num < 0:
                        word_num_dict[wordstem] = word_count
                        num_word_dict[word_count] = wordstem
                        index_dict[word_count] = {page_number: [word_position]}

                        if term_frequency_max < 1: term_frequency_max = 1

                        word_count += 1

                    # word ALREADY in the index, word NOT YET in the page
                    elif word_num >= 0 and page_number not in index_dict[word_num]:
                        index_dict[word_num] = {**index_dict[word_num], **{page_number: [word_position]}}

                    # word ALREADY in the index, word ALREADY in the page
                    elif word_num >= 0 and page_number in index_dict[word_num]:
                        index_dict[word_num][page_number] += [word_position]

                        if term_frequency_max < len(index_dict[word_num][page_number]):
                            term_frequency_max = len(index_dict[word_num][page_number])

                    # ERROR
                    else:
                        raise Exception('Issue with word: "{}" \n\tin the page {} \n\tat the position {}'.format(wordstem, page_number, word_position))

        # total nb of words
        infos_doc_dict[page_number][0] = word_position

        # term frequency max
        infos_doc_dict[page_number][1] = term_frequency_max

    return index_dict, word_num_dict, num_word_dict, infos_doc_dict

if __name__ == '__main__':
    pass