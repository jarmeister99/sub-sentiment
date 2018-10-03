import string


def main():
    # prompt_option()
    c = Classifier(['apple28', 'granRo-la'])
    c.record_sentence_sentiment("How can I help you today Mr. Jones?", "POSITIVE")


# displays the options the user can choose and prompt for one
# RETURN: character (representing an action)
def prompt_option():
    while True:
        print("Options:")
        print("T(rain)")
        print("Q(uery")
        print("O(verview)")
        response = input(">")
        if response.lower() in 'tqd' and len(response) == 1:
            return response
        else:
            print("Please choose from one of the options")


class Classifier():
    def __init__(self, word_list):
        self.word_list = word_list

        # word -> {pos: num, neg: num}
        self.sentiment_map = {}

        self.initialize()

    # ensures punctuation and numbers are stripped from all entries
    # RETURN: None
    def clean_words(self):
        self.word_list = []
        for word in self.word_list:
            self.word_list.append(
                self.clean_word(word))

    # ensure punctuation and numbers are stripped from the input string
    # RETURN: cleaned string
    def clean_word(self, s):
        return s.rstrip().translate(str.maketrans('', '', string.punctuation + string.digits)).lower()

    # loads words from internal word map to internal sentiment map
    # RETURN: None
    def load_sentiment_map(self):
        self.clean_words()
        for word in self.word_list:
            if word not in self.sentiment_map.keys():
                self.sentiment_map[word] = {'positive': 0,
                                            'negative': 0}
                self.word_list.remove(word)

    # loads words from given list to internal word map
    # RETURN: None
    def load_words(self, words):
        for word in words:
            if word not in self.sentiment_map.keys():
                self.word_list.append(word)

    # increment the appropriate sentiment value for each word in the given sentence
    # RETURN: None
    def record_sentence_sentiment(self, s, sentiment):
        self.load_words(s.split())
        self.clean_words()
        for word in s.split():
            if self.clean_word(word) in self.sentiment_map.keys():
                self.sentiment_map[word][sentiment.lower()] += 1

    # export dictionary to file


    def __str__(self):
        return str(self.word_list)


if __name__ == "__main__":
    main()
