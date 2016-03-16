from __future__ import division

import random
import re
from collections import defaultdict

from language_processing import LanguageProcessor
from scrapers import Scraper


class StringContinuationImpossibleError(Exception):
    pass


lang_proc = LanguageProcessor.LanguageProcessor()
scraper = Scraper.Scraper()


class SubjectModel(object):
    def __init__(self, name):
        """
        Constructor for a SubjectModel
        :param name: The word to base the SubjectModel off of
        :return: Nada
        """

        self.name = name
        self.db = _db_factory()
        self.sample_text = ""
        self.word_counts = []

    def setup_model_db(self, sentence_separator='[.!?\n]', n=2, source='wikipedia'):
        """
        Generate a MarkovChain model for the requested word.
        :param sentence_separator: A list of different seperators for sentences
        :param n:
        :param source: The source of information to scrape from
        :return: Saves the model
        """
        """ Generate word probability database from raw content string """
        # I'm using the database to temporarily store word counts

        if source == 'wikipedia':
            self.sample_text = scraper.get_content(self.name, source)

        textSample = _wordIter(self.sample_text,
                               sentence_separator)  # get an iterator for the 'sentences'

        self.word_counts = lang_proc.get_word_count(self.sample_text)
        # We're using '' as special symbol for the beginning
        # of a sentence
        self.db[('',)][''] = 0.0
        for line in textSample:
            words = line.strip().split()  # split words in line
            if len(words) == 0:
                continue
            # first word follows a sentence end
            self.db[("",)][words[0]] += 1

            for order in range(1, n + 1):
                for i in range(len(words) - 1):
                    if i + order >= len(words):
                        continue
                    word = tuple(words[i:i + order])
                    self.db[word][words[i + order]] += 1

                # last word precedes a sentence end
                self.db[tuple(words[len(words) - order:len(words)])][""] += 1

        # We've now got the db filled with parametrized word counts
        # We still need to normalize this to represent probabilities
        for word in self.db:
            wordsum = 0
            for nextword in self.db[word]:
                wordsum += self.db[word][nextword]
            if wordsum != 0:
                for nextword in self.db[word]:
                    self.db[word][nextword] /= wordsum

    def generate_string(self):
        """
        Generate a "sentence" with the database of known text
        :return:
        """
        return self._accumulate_with_seed(('',))

    def generate_seed_with_string(self, seed):
        """
        Generate a "sentence" with the database and a given word
        :param seed: The word to base the sentence off of
        :return:
        """
        # using str.split here means we're contructing the list in memory
        # but as the generated sentence only depends on the last word of the seed
        # I'm assuming seeds tend to be rather short.
        words = seed.split()
        if (words[-1],) not in self.db:
            # The only possible way it won't work is if the last word is not known
            raise StringContinuationImpossibleError('Could not continue string: '
                                                    + seed)
        return self._accumulate_with_seed(words)

    def _accumulate_with_seed(self, seed):
        """
        Accumulate the generated sentence with a given single word as a seed
        :param seed: The word to base the sentence off of
        :return:
        """
        nextWord = self._next_word(seed)
        sentence = list(seed) if seed else []
        while nextWord:
            sentence.append(nextWord)
            nextWord = self._next_word(sentence)
        return ' '.join(sentence).strip()

    def _next_word(self, lastwords):
        """
        Iterate through the itemized words
        :param lastwords:
        :return:
        """
        lastwords = tuple(lastwords)
        if lastwords != ('',):
            while lastwords not in self.db:
                lastwords = lastwords[1:]
                if not lastwords:
                    return ''
        probmap = self.db[lastwords]
        sample = random.random()
        # since rounding errors might make us miss out on some words
        maxprob = 0.0
        maxprobword = ""
        for candidate in probmap:
            # remember which word had the highest probability
            # this is the word we'll default to if we can't find anything else
            if probmap[candidate] > maxprob:
                maxprob = probmap[candidate]
                maxprobword = candidate
            if sample > probmap[candidate]:
                sample -= probmap[candidate]
            else:
                return candidate
        # getting here means we haven't found a matching word. :(
        return maxprobword


# We have to define these as separate functions so they can be pickled.
def _db_factory():
    return defaultdict(_one_dict)


def _one():
    return 1.0


def _one_dict():
    return defaultdict(_one)


def _wordIter(text, separator='.'):
    """
    An iterator over the 'words' in the given text, as defined by
    the regular expression given as separator.
    :param text: The text to iterate over
    :param separator: The seperator to focus on
    :return:
    """
    exp = re.compile(separator)
    pos = 0
    for occ in exp.finditer(text):
        sub = text[pos:occ.start()].strip()
        if sub:
            yield sub
        pos = occ.start() + 1
    if pos < len(text):
        # take case of the last part
        sub = text[pos:].strip()
        if sub:
            yield sub
