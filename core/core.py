# -*- coding: utf-8 -*-

import os
import time
import collections
import libs.kea as kea
from tqdm import tqdm


def collect_datadoc_dict():
    """
    Returns a dict containing file num as key, file content as value.
    """
    dir = 'data/lemonde-utf8'
    os.chdir('..')

    dict = {}
    for i,filename in enumerate(os.listdir(dir)):
        path = '{}/{}'.format(dir, filename)
        with open(path, 'r') as infile:
            dict[i] = infile.read()

    return dict


def index_creation(datadoc):
    """
    Creates and return the positional index for all the files in the datadoc.
    """
    keatokenizer = kea.tokenizer()

    stopwords_file = open('data/stopwords-fr.txt', 'r')
    stopwords = []
    for stopword in stopwords_file:
        stopwords.append(stopword.split()[0])
    stopwords = set(stopwords)

    index = {}

    for page in datadoc.keys():

        i = 0
        for line in datadoc[page].split('\n'):
            words = keatokenizer.tokenize(line)

            for word in words:
                if word not in stopwords:
                    i=i+1
                    word = word.lower()
                    if word in index.keys() and page in index[word]:
                        index[word][page]=[i]+index[word][page]
                    elif word in index.keys():
                        index[word] = {**index[word],**{page : [i]}}
                    else:
                        index[word]={page : [i]}

    return index


def main():

    datadict = collect_datadoc_dict()

    print(datadict[1])

    #index
    index=index_creation(datadict)

    print(index)


if __name__ == '__main__':
    time0 = time.time()

    main()

    duration = time.time() - time0

    print("Temps d'execution = {} seconde(s)\n".format(duration))
