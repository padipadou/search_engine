# -*- coding: utf-8 -*-

import os
import time
import collections
import kea.kea as kea
from tqdm import tqdm

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

    for line in input_file:
        #words = line.split()

        keatokenizer = kea.tokenizer()
        words = keatokenizer.tokenize(line)

        for word in words:
            word = word.lower()
            if word not in stopwords:
                if not word in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] = word_count[word] + 1

    input_file.close()

    return word_count

def main():
    dir = 'data/lemonde-utf8'
    os.chdir('..')
    word_count = {}

    for filename in tqdm(os.listdir(dir)):
        word_count_update = word_count_dict('{}/{}'.format(dir, filename))

        #merge
        first = collections.Counter(word_count)
        second = collections.Counter(word_count_update)
        word_count = dict(first + second)

    word_count_list = sorted(word_count.items(), key=lambda t: t[1])
    print('{}'.format(word_count_list[-1::-21]))

if __name__ == '__main__':
    time0 = time.time()

    main()
    duration = time.time() - time0

    print("Temps d'execution = {} seconde(s)\n".format(duration))
