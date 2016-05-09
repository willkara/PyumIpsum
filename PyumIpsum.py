import json

import wikipedia
from flask import Flask, Response, request, render_template
from flask_restful import Api, Resource

import settings
from generators import SentenceGenerator

application = Flask(__name__)

api = Api(application)
gen = SentenceGenerator.SentenceGenerator()


@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')


class Info(Resource):
    """
    The RESTful class endpoint that handles Info about the system
    """

    @staticmethod
    def get():
        """
        Generates and returns basic Info about the system.
        :return:
        """
        return {'subject_count': gen.cache.get_total()}


class Subject(Resource):
    """
    The RESTful class endpoint that handles subject sentence generation
    """

    @staticmethod
    def get(word):
        """
        Generate and return a JSON reponse with:
            subject: The word requested
            sentence: The generated sentence
            common_words: An array of the 10 most common words and their counts

        :param word: The word to generate a sentence about
        :request num: The number of sentences to generate
        :return: A JSON response with:
            subject: The word requested
            sentence: The generated sentence
            common_words: An array of the 10 most common words and their counts
        """
        try:
            sentence_amount = request.args.get('num', 1)
            model = gen.generate_model(word)
            sentences = []

            for i in range(0, int(sentence_amount)):
                sentences.append(model.generate_string())

            data = {}
            data['status'] = '0'
            data['sentences'] = sentences
            data['common_words'] = model.word_counts
        except wikipedia.exceptions.DisambiguationError as dis:

            data = {}
            data['status'] = '1'
            data['error'] = dis.error

        return Response(json.dumps(data), mimetype='application/json')


# Main entry point for the program
api.add_resource(Subject, '{0}/subject/<word>'.format(settings.API_URL))
api.add_resource(Info, '/{0}/info'.format(settings.API_URL))

if __name__ == '__main__':
    application.run(debug=settings.DEBUG, port=settings.PORT)
