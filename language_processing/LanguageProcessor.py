import re

from nltk import FreqDist, corpus

# Taken from http://www.strehle.de/tim/weblog/archives/2015/09/03/1569

stopword_set = set(corpus.stopwords.words('english'))


class LanguageProcessor(object):
    def __init__(self):
        pass

    def get_word_count(self, content, size=10):
        """
        Return a list of the most common words (sans stop words) within a given text.
        :param content: The text to go over.
        :param size: The number of words to return
        :return: A list of the most common words (sans stop words) within a given text.
        """
        content = filter(lambda x: x.lower() not in stopword_set,
                         re.findall(r'\w+', content, flags=re.UNICODE | re.LOCALE))
        freq = FreqDist(content)
        return freq.most_common(size)
