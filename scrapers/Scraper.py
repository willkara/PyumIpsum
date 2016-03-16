import wikipedia


class Scraper(object):
    def __init__(self):
        pass

    def get_content(self, term, source='wikipedia'):
        if source == 'wikipedia':
            return self._get_wikipedia_content(term)

    @staticmethod
    def _get_wikipedia_content(keyword):
        """
        Scrape and return the content of a wikipedia page.
        :param keyword: The keyword to search for.
        :return: The content of a wikipedia page.
        """
        text = wikipedia.page(keyword).content
        return text
