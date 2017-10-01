# -*- coding: utf-8 -*-

import os
import time
import collections
import libs.kea as kea
from tqdm import tqdm


def load_data_dict():
    """
    Returns a dict containing file num as key, file content as value.
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
    Creates and returns the positional index for all the files in the datadoc.
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

    for page_number in datadict.keys():

        i = 0
        for line in datadict[page_number].split('\n'):
            words = tokenizer.tokenize(line)

            for word in words:
                if word not in stopwords:
                    i += 1
                    word = word.lower()
                    if word in index_dict.keys() and page_number in index_dict[word]:
                        index_dict[word][page_number] += [i]

                    elif word in index_dict.keys():
                        index_dict[word] = {**index_dict[word],**{page_number : [i]}}

                    else:
                        index_dict[word] = {page_number : [i]}

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
