from multiprocessing import Process, Pipe, Queue
from tqdm import tqdm

import src.search_engine.sub_steps.normalization as nrm
import src.search_engine.sub_steps.handle_data as hd
import src.other.pickle_usage as pck
import src.other.memory_usage as mem
from src import Const
import libs.kea as kea


def get_total_word_nb(alpha_dict):
    """
    :param alpha_dict: alpha_dict with letters as key, number of words with this these first letters
    :return: sum of all values from alpha_dict
    """
    total_word_nb = 0
    for val_ in alpha_dict.values():
        total_word_nb += val_

    return total_word_nb


def creation_alpha_dict(depth):
    """
    Returns a dict with the beginning of each word regarding the depth
    :param depth: numbers of first letters to look at
    :return: alpha_dict
    """
    alphabet_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    alpha_dict = {}

    if depth == 1:
        for first_letter in alphabet_list:
            key_ = first_letter
            alpha_dict[key_] = 0
    elif depth == 2:
        for first_letter in alphabet_list:
            for second_letter in alphabet_list:
                key_ = first_letter + second_letter
                alpha_dict[key_] = 0
    elif depth == 3:
        for first_letter in alphabet_list:
            for second_letter in alphabet_list:
                for third_letter in alphabet_list:
                    key_ = first_letter + second_letter + third_letter
                    alpha_dict[key_] = 0
    elif depth == 4:
        for first_letter in alphabet_list:
            for second_letter in alphabet_list:
                for third_letter in alphabet_list:
                    for fourth_letter in alphabet_list:
                        key_ = first_letter + second_letter + third_letter + fourth_letter
                        alpha_dict[key_] = 0
    else:
        print("Too deep for now.")
        return alpha_dict

    # for words with accents
    alpha_dict["0others"] = 0

    return alpha_dict


def repartition_corpus(nb_docs_to_look_at=100, depth=2):
    """
    counter of words regarding first letters, using same normalization as real search engine
    :param nb_docs_to_look_at: the more we put in it, the precise it will be
    :param depth: the more we put in it, the precise it will be (number of first letters to check)
    :return: alpha_dict with number of words for each beginning of word (key)
    """
    if 0 < depth < 5:
        alpha_dict = creation_alpha_dict(depth)
    else:
        print("Error with depth.")
        return {}

    data_dict, num_name_dict = \
        hd.load_data_dict(Const.DIRECTORY_NAME, nb_docs_to_look_at)

    # useless data
    del num_name_dict

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    stopwords = hd.load_stopwords_set('data/stopwords-fr.txt')

    for page_number in tqdm(data_dict.keys()):
        content_page = data_dict[page_number].split('\n')
        for line in content_page:
            words_line = tokenizer.tokenize(line)
            for word in words_line:
                norm_word = nrm.normalization(word, stopwords)
                if norm_word is not None:
                    key_ = norm_word[:depth]

                    if alpha_dict.get(key_, -1) >= 0:
                        alpha_dict[key_] += 1
                    else:
                        alpha_dict["0others"] += 1

    return alpha_dict


def repartition_groups_calc(alpha_dict, groups_nb):
    """
    try to estimate best distribution to create the number of group that you really need
    :param alpha_dict: number of words for each beginning of word (key)
    :param groups_nb: desired number of groups
    :return: list with each beginning/end of group and size in percentage
    - start_key
    - prev_key
    - val_nb: number of words in this category
    - val_nb / total_word_nb: percentage of words in this category
    """
    total_word_nb = get_total_word_nb(alpha_dict)
    val_nb_group = int(total_word_nb / (groups_nb - 1))

    # last group for other words
    other_words_value = alpha_dict["0others"]
    del alpha_dict["0others"]

    val_nb = 0
    start_end_groups = []
    start_key = "0000000000"

    for key, value in sorted(alpha_dict.items(), key=lambda x: x[0], reverse=False):
        val_nb += value
        if val_nb > val_nb_group:
            start_end_groups.append([start_key, prev_key, prev_val, prev_val / total_word_nb])
            start_key = key
            val_nb = value
        prev_key = key
        prev_val = val_nb

    # last normal group
    if val_nb > 0:
        start_end_groups.append([start_key, prev_key, val_nb, val_nb / total_word_nb])

    # last group for other words
    start_end_groups.append(["0others", other_words_value, other_words_value / total_word_nb])

    return start_end_groups


def alphabet_repartition(nb_docs_to_look_at, depth, groups_nb, memory_tracker):
    """
    create start_end_groups and store it
    :param nb_docs_to_look_at: the more we put in it, the precise it will be
    :param depth: the more we put in it, the precise it will be (number of first letters to check)
    :param groups_nb: desired number of groups
    :return: start_end_groups: list of list with start_key, prev_key, number of words, percentage
    """
    if memory_tracker:
        print("Memory tracker activated.")
        time_gap = 0.01
        phase_name = "alphabet_repartition"
        q = Queue()
        p = Process(target=mem.track_memory_usage, args=(phase_name, time_gap, q))
        p.start()

    alpha_dict = repartition_corpus(nb_docs_to_look_at, depth)
    start_end_groups = repartition_groups_calc(alpha_dict, groups_nb)

    repartition_max_percent = 0
    for start_end_group in start_end_groups:
        if start_end_group[-1] > repartition_max_percent:
            repartition_max_percent = start_end_group[-1]

    pck.pickle_store("start_end_groups", start_end_groups, "")

    if memory_tracker:
        q.put("STOP_SIGNAL!")
        p.join()

    print("Repartition in", groups_nb, "groups for first", nb_docs_to_look_at, "documents with", depth,
          "letter(s) have been done correctly.")


if __name__ == '__main__':
    depth = 3
    groups_nb = 27
    nb_docs_to_look_at = 1000

    alphabet_repartition(nb_docs_to_look_at, depth, groups_nb, False)
