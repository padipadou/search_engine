# -*- coding: utf-8 -*-

import os
import time
from collections import Counter

def word_count_dict(filename):
    """
    Returns a word/count DICT for this filename.
    """

    word_count_update = {}
    input_file = open(filename, 'r')

    for line in input_file:
        words = line.split()
        for word in words:
            word = word.lower()
            if not word in word_count_update:
                word_count_update[word] = 1
            else:
                word_count_update[word] = word_count_update[word] + 1

    input_file.close()

    return word_count_update

def main():
    dir = 'data/lemonde-utf8'
    os.chdir('..')
    word_count = {}

    for filename in os.listdir(dir):
        word_count_update = word_count_dict('{}/{}'.format(dir, filename))

        #merge
        first = Counter(word_count)
        second = Counter(word_count_update)
        word_count = dict(first + second)

    word_count_list = sorted(word_count.items(), key=lambda t: t[1])
    print(word_count_list[-1::-21])

if __name__ == '__main__':
    time0 = time.time()

    main()
    duration = time.time() - time0

    print "Temps d'execution = {} seconde(s)\n".format(duration)
