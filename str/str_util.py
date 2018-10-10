from string import punctuation
from statistics import mode, median, StatisticsError


# calculate the average word length of a sentence
# INPUT: string sentence
# RETURN: average word length
def get_average_word_length(sentence):
    total_letters = 0
    total_words = 0
    words = clean(sentence).split()
    for word in words:
        total_words += 1
        total_letters += len(word)
    return total_letters / total_words


# find the median word length of a sentence
# INPUT: string sentence
# RETURN: median word length
def get_median_word_length(sentence):
    words = clean(sentence).split()
    list_of_lengths = [len(word) for word in words]
    return median(list_of_lengths)


# calculate the modal word length of a sentence
# INPUT: string sentence
# RETURN: int mode
def get_mode_word_length(sentence):
    words = clean(sentence).split()
    list_of_lengths = [len(word) for word in words]
    try:
        return mode(list_of_lengths)
    except StatisticsError:
        print('Info: No mode found')
        return -1


# find the modal word of a sentence
# INPUT: string sentence
# RETURN: string mode
def get_mode_word(sentence):
    words = clean(sentence).split()
    try:
        return mode(words)
    except StatisticsError:
        print('Info: No mode found')
        return ''


# read contractions.txt and create a list from the entries
# OPTIONAL INPUT: path to file containing contractions
# RETURN: a list of comment english contractions
def get_contractions(path='contractions.txt'):
    contractions = []
    with open(path, 'r') as f:
        entries = [line.rstrip('\n') for line in f.readlines()]
        for entry in entries:
            contractions.append(entry)
    return contractions


# splits string by punctuation while maintaining contractions
# INPUT: string sentence, list of contractions
# RETURN: list of strings
def split_by_punctuation(sentence, contractions):
    # first split by space
    words = sentence.split(' ')
    for i in range(len(words)):

        # if the word contains any punctuation
        if any(p in words[i] for p in punctuation):

            # check if the word is a real contraction
            if not words[i].lower() in contractions:
                # break up the fake contraction
                pieces = ''.join((char if char.isalpha() else ' ') for char in words[i]).split()
                words[i] = pieces[0]
                words.insert(i + 1, pieces[1])
    return words


# INPUT: string sentence, int index
# RETURN: the strings in indeces (i - 1, i + 1)
def get_neighbors(sentence, index):
    # preserve punctuation in the sentence
    words = split_by_punctuation(sentence, get_contractions())

    # case where words is empty
    if not words:
        print('Error: Sentence is empty')
        raise StringError()

    # case where given index is 0
    try:
        if index == 0:
            return None, words[index + 1]
    except IndexError:
        print('Error: Not enough words given')

    # case where given index is the last index in string
    if index == len(words) - 1:
        return words[index - 1], None

    # general case
    return words[index - 1], words[index + 1]


# cleans a string by removing punctuation and trailing whitespace
# RETURN: cleaned string
def clean(s):
    return s.translate(str.maketrans('', '', punctuation)).rstrip().lower()


# make a string suitable for SQLite db
# RETURN: barely cleaned string
def soft_clean(s):
    return s.replace("'", "`")


class StringError(Exception):
    pass
