import string


# cleans a string by removing punctuation and trailing whitespace
# RETURN: cleaned string
def clean(s):
    return s.translate(str.maketrans('', '', string.punctuation)) \
        .rstrip()

def connect_reddit():
    pass
