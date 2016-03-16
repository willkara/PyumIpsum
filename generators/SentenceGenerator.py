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

    def generate_model(self, subject):
        """
        Generate a model for the specified subject/word
        :param subject: The subject/word to base the model off of.
        :return: A SubjectModel object.
        """
        try:
            subject_model = self.cache.get(subject)

            if subject_model is None:
                subject_model = SubjectModel.SubjectModel(subject)
                subject_model.setup_model_db()
                self.cache.add(subject, subject_model)

            return subject_model
        except wikipedia.exceptions.DisambiguationError as e:
            raise
