# -*- coding: utf-8 -*-

import os
import time
import collections
import kea.kea as kea
from tqdm import tqdm

def collect_datadoc_dict():
    dir = 'data/lemonde-utf8'
    os.chdir('..')

    dict = {}
    for i,filename in enumerate(os.listdir(dir)):
        path = '{}/{}'.format(dir, filename)
        with open(path, 'r') as infile:
            dict[i] = infile.read()

    return dict


def word_count_dict(filename):
    """
    Returns a word/count DICT for this filename.
    """

    word_count = {}
    input_file = open(filename, 'r')
    stopwords_file = open('data/stopwords-fr.txt', 'r')
    stopwords = []
    for stopword in stopwords_file:
        stopwords.append(stopword.split()[0])
    stopwords = set(stopwords)

    keatokenizer = kea.tokenizer()

    for line in input_file:
        words = line.split()

        #words = keatokenizer.tokenize(line)

        # for word in words:
        #     word = word.lower()
        #     if word not in stopwords:
        #         if not word in word_count:
        #             word_count[word] = 1
        #         else:
        #             word_count[word] = word_count[word] + 1

    input_file.close()

    return word_count


def transform_page_names_into_numbers(dir):
    """
    Creates a dictionnary (dico) where the keys are the document names (strings) and the values are numbers
    """
    dico = {}

    i=1
    for filename in tqdm(os.listdir(dir)):
        dico['{}/{}'.format(dir, filename)]=i
        i=i+1

    return dico


def one_document_index_creation(filename,dico):
    """
    Creates and return an index for this filename.
    """

    index = {}
    input_file = open(filename, 'r')
    stopwords_file = open('data/stopwords-fr.txt', 'r')
    stopwords = []
    for stopword in stopwords_file:
        stopwords.append(stopword.split()[0])
    stopwords = set(stopwords)

    for line in input_file:

        keatokenizer = kea.tokenizer()
        words = keatokenizer.tokenize(line)

        for word in words:
            word = word.lower()
            if word not in stopwords:
                doclist = index.get(word, )

                index[word] = count + 1
                if not word in index:
                    index[word] = [dico[filename]]
                else:
                    index[word] = index[word]+[dico[filename]]

    input_file.close()

    return index


def index_creation(dir,dico):
    """
    Creates and return the index for all the files in the directory.
    """

    index_update = {}

    for filename in tqdm(os.listdir(dir)):
        index_temp = one_document_index_creation('{}/{}'.format(dir, filename),dico)

        for word in index_temp.keys():
            if word in index_update:
                index_update[word] = index_update[word] + index_temp[word]
            else:
                index_update[word] = index_temp[word]

    index = {}

    for key, value in index_update.items():
        list_of_tuples = [(x, value.count(x)) for x in set(value)]
        index[key] = list_of_tuples

    return index


def main():

    datadict = collect_datadoc_dict()

    print(datadict[1])

    #dir = 'data/lemonde-utf8'
    #os.chdir('..')

    #word_count
    #word_count = {}

    # for filename in tqdm(os.listdir(dir)):
    #     word_count_update = word_count_dict('{}/{}'.format(dir, filename))
    #
    #     # merge
    #     first = collections.Counter(word_count)
    #     second = collections.Counter(word_count_update)
    #     word_count = dict(first + second)
    #
    # word_count_list = sorted(word_count.items(), key=lambda t: t[1])
    # print('{}'.format(word_count_list[-1::-21]))

    #dico=transform_page_names_into_numbers(dir);

    #index
    # index=index_creation(dir,dico)
    #
    # print("Display of the index:")
    #
    # for key,value in index.items():
    #     print("{}->{}".format(key,value))
    #
    # print("\nDisplay of dico:")
    # dico_list = sorted(dico.items(), key=lambda t: t[1])
    # print('{}'.format(dico_list))


if __name__ == '__main__':
    time0 = time.time()

    main()

    duration = time.time() - time0

    print("Temps d'execution = {} seconde(s)\n".format(duration))
