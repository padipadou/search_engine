# -*- coding: utf-8 -*-

import os
import time
import libs.kea as kea
import tqdm as tq


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


def create_index_dict(datadict):
    """
    Creates and returns the positional index for all the files in datadict.
    Creates and returns a dict containing word num as key, word as value for all the words in datadict.
    """
    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    # stopwords set
    stopwords_file = open('../data/stopwords-fr.txt', 'r')
    stopwords = []
    for stopword in stopwords_file:
        stopwords.append(stopword.split()[0])
    stopwords = set(stopwords)

    index_dict = {}
    #word_num_dict = {}

    for page_number in tq.tqdm(datadict.keys()):
        word_position = 0
        content_page = datadict[page_number].lower().split('\n')

        for line in content_page:
            # faster to do it line by line than page by page
            words_line = tokenizer.tokenize(line)

            for word in words_line:

                if word not in stopwords:
                    word_position += 1

                    # word already in the index, word already in the page
                    if word in index_dict.keys() and page_number in index_dict[word]:
                        index_dict[word][page_number] += [word_position]

                    # word already in the index, word NOT YET in the page
                    elif word in index_dict.keys():
                        index_dict[word] = {**index_dict[word], **{page_number: [word_position]}}

                    # word NOT YET in the index, word NOT YET in the page
                    elif word not in index_dict.keys():
                        index_dict[word] = {page_number: [word_position]}

                    else:
                        raise Exception('Issue with word: "{}" \n\tin the page {} \n\tat the position {}'.format(word, page_number, word_position))

    return index_dict


def main():
    print("Loading data...")
    datadict = load_data_dict()

    print("Creating index...")
    index = create_index_dict(datadict)

    print(index)


if __name__ == '__main__':
    time0 = time.time()

    main()

    duration = time.time() - time0

    print("Temps d'execution = {} seconde(s)\n".format(duration))
