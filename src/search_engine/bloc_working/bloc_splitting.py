import src.search_engine.pickle_usage as pck

import os
from os import remove


def split_indexes(bloc_num, start_end_groups):  # MAYBE NEED TO IMPROVED WITH PROCESSES

    depth = len(start_end_groups[0][0])

    path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
    index_dict = pck.pickle_load(path_name, "")
    path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
    word_num_dict = pck.pickle_load(path_name, "")

    for sub_bloc_num, start_end_group in enumerate(start_end_groups):
        os.mkdir("data/pickle_files/b_{}/b_{}_{}".format(bloc_num, bloc_num, sub_bloc_num))
        sub_index_dict = {}
        sub_word_num_dict = {}
        sub_num_word_dict = {}

        # we have some letters
        if start_end_group[0] != "0others":
            start_key = start_end_group[0]
            end_key = start_end_group[1]
        # other words
        else:
            start_key = False
            end_key = False

        # useless to sort... but mandatory
        sorted_items = sorted(word_num_dict.items(), key=lambda x: x[0], reverse=False)
        # items_ = word_num_dict.items() # ISSUE HERE: RuntimeError: dictionary changed size during iteration
        for key, value in sorted_items:
            if start_key and end_key:
                first_letters = key[:depth]
                if start_key <= first_letters <= end_key:
                    need_to_add = True
                else:
                    need_to_add = False
            else:
                need_to_add = True

            if need_to_add:
                sub_word_num_dict[key] = value
                sub_num_word_dict[value] = key
                sub_index_dict[value] = index_dict[value]
                del word_num_dict[key]

        # print("Memory usage", memory_usage(), "Mo", start_key)

        path_name = "b_{}/b_{}_{}/word_num_dict_b{}_{}".format(bloc_num,
                                                               bloc_num, sub_bloc_num,
                                                               bloc_num, sub_bloc_num)
        pck.pickle_store(path_name, sub_word_num_dict, "")
        path_name = "b_{}/b_{}_{}/num_word_dict_b{}_{}".format(bloc_num,
                                                               bloc_num, sub_bloc_num,
                                                               bloc_num, sub_bloc_num)
        pck.pickle_store(path_name, sub_num_word_dict, "")
        path_name = "b_{}/b_{}_{}/index_dict_b{}_{}".format(bloc_num,
                                                            bloc_num, sub_bloc_num,
                                                            bloc_num, sub_bloc_num)
        pck.pickle_store(path_name, sub_index_dict, "")

    path_name = "b_{}/index_dict_b{}".format(bloc_num, bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/word_num_dict_b{}".format(bloc_num, bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")
    path_name = "b_{}/num_word_dict_b{}".format(bloc_num, bloc_num)
    remove("data/pickle_files/" + path_name + ".pickle")


if __name__ == '__main__':
    pass
