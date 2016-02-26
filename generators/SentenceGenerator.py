import wikipedia

from dataobjects import SubjectModel
from datastore import Cache


class SentenceGenerator(object):
    def __init__(self):
        """
        Create an instance of the SentenceGenerator
        :return:
        """
        self.cache = Cache.Cache()

    def generateModel(self, subject):
        """
        Generate a model for the specified subject/word
        :param subject: The subject/word to base the model off of.
        :return: A SubjectModel object.
        """
        try:
            subjectModel = self.cache.get(subject)

            if subjectModel is None:
                subjectModel = SubjectModel.SubjectModel(subject)
                subjectModel.setup_model_db()
                self.cache.add(subject, subjectModel)

            return subjectModel
        except wikipedia.exceptions.DisambiguationError as e:
            raise
