import core_functions.handle_data as hd
import core_functions.pickle_usage as pck
import core_functions.normalization as nrm
import libs.kea as kea
import tqdm as tq


def creation_alpha_dict(depth):
    alphabet_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                     "u", "v", "w", "x", "y", "z"]
    alpha_dict = {}
    for first_letter in alphabet_list:
        if depth == 1:
            key_ = first_letter
            alpha_dict[key_] = 0
        elif depth == 2:
            for second_letter in alphabet_list:
                key_ = first_letter + second_letter
                alpha_dict[key_] = 0
        elif depth == 3:  # NOT USED FOR THE MOMENT
            for second_letter in alphabet_list:
                for third_letter in alphabet_list:
                    key_ = first_letter + second_letter + third_letter
                    alpha_dict[key_] = 0

    alpha_dict["0others"] = 0

    return alpha_dict


def repartition_corpus(nb_docs_to_look_at=100, depth=2):
    if 0 < depth < 4:
        alpha_dict = creation_alpha_dict(depth)
    else:
        print("Error with depth.")
        return {}

    data_dict, name_num_dict, num_name_dict = \
        hd.load_data_dict("../../data/text_10000", nb_docs_to_look_at)

    # useless data
    del name_num_dict
    del num_name_dict

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    stopwords = hd.load_stopwords_set('../../data/stopwords-fr.txt')

    for page_number in tq.tqdm(data_dict.keys()):
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
    total_word_nb = get_total_word_nb(alpha_dict)
    val_nb_group = int(total_word_nb/groups_nb)

    val_nb = 0
    start_end_groups = []
    start_key = "00"
    for key, value in sorted(alpha_dict.items(), key=lambda x: x[0], reverse=False)[1:]:
        val_nb += value
        if val_nb > val_nb_group:
            start_end_groups.append([start_key, prev_key, val_nb, val_nb / total_word_nb])
            start_key = key
            val_nb = value
        prev_key = key
    if val_nb > 0:
        start_end_groups.append([start_key, prev_key, val_nb, val_nb/total_word_nb])

    val_nb = alpha_dict["0others"]
    start_end_groups.append(["0others", val_nb, val_nb/total_word_nb])

    return start_end_groups


def get_total_word_nb(alpha_dict):
    total_word_nb = 0
    for val_ in alpha_dict.values():
        total_word_nb += val_

    return total_word_nb


def write_csv(alpha_dict, total_word_nb):
    f = open('../../data/alphabet_repartition.csv', 'w')

    for key, value in sorted(alpha_dict.items(), key=lambda x: x[0], reverse=False):
        row = "{};{}\n".format(key, value/total_word_nb)
        f.write(row)

    f.close()


if __name__ == '__main__':
    # alpha_dict = repartition_corpus(depth=3)
    # pck.pickle_store("alpha_dict", alpha_dict, "../../")

    alpha_dict = pck.pickle_load("alpha_dict", "../../")

    groups_nb = 50
    start_end_groups = repartition_groups_calc(alpha_dict, groups_nb)
    for start_end_group in start_end_groups:
        print(start_end_group)
