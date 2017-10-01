import libs.kea as kea
import tqdm as tq

def create_index_dict(datadict, stopwords):
    """
    Creates and returns the positional index for all the files in datadict.
    Creates and returns a dict containing a word as key, wordnum as value for all the words in datadict.
    Creates and returns a dict containing a wordnum as key, word as value for all the words in datadict.
    """
    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    word_num_dict = {}
    num_word_dict = {}
    index_dict = {}
    word_count = 0

    for page_number in tq.tqdm(datadict.keys()):
        word_position = 0
        content_page = datadict[page_number].lower().split('\n')

        for line in content_page:
            # faster to do it line by line than page by page
            words_line = tokenizer.tokenize(line)

            for word in words_line:

                if word not in stopwords:
                    word_position += 1

                    word_num = word_num_dict.get(word)

                    # word NOT YET in the index, word NOT YET in the page
                    if not word_num :
                        word_num_dict[word] = word_count
                        num_word_dict[word_count] = word
                        index_dict[word_count] = {page_number: [word_position]}

                        word_count += 1

                    # word ALREADY in the index, word NOT YET in the page
                    elif word_num and page_number not in index_dict[word_num]:
                        index_dict[word_num] = {**index_dict[word_num], **{page_number: [word_position]}}

                    # word ALREADY in the index, word ALREADY in the page
                    elif word_num and page_number in index_dict[word_num]:
                        index_dict[word_num][page_number] += [word_position]

                    # ERROR
                    else:
                        raise Exception('Issue with word: "{}" \n\tin the page {} \n\tat the position {}'.format(word, page_number, word_position))

    return index_dict, word_num_dict, num_word_dict

if __name__ == '__main__':
    pass