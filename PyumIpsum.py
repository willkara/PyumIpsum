import json

import wikipedia
import settings
from flask import Flask, Response, request, render_template
from flask_restful import Api, Resource

from generators import SentenceGenerator

application = Flask(__name__)

api = Api(application)
gen = SentenceGenerator.SentenceGenerator()


@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')


class info(Resource):
    """
    The RESTful class endpoint that handles info about the system
    """


    def get(self):
        """
        Generates and returns basic info about the system.
        :return:
        """
        return {'subject_count': gen.cache.get_total()}



class subject(Resource):
    """
    The RESTful class endpoint that handles subject sentence generation
    """

    def get(self, word):
        """
        Generate and return a JSON reponse with:
            subject: The word requested
            sentence: The generated sentence
            common_words: An array of the 10 most common words and their counts

        :param word: The word to generate a sentence about
        :request num: The number of sentences to generate
        :return: A JSON reponse with:
            subject: The word requested
            sentence: The generated sentence
            common_words: An array of the 10 most common words and their counts
        """
        try:
            sentenceAmount = request.args.get('num', 1)
            model = gen.generateModel(word)
            sentences = []

            for i in range(0, int(sentenceAmount)):
                sentences.append(model.generateString())

            data = {'status': "0",
                    'sentences': sentences,
                    'common_words': model.word_counts
                    }
        except wikipedia.exceptions.DisambiguationError as dis:
            data = {'status': "1",
                    'error': "wikipedia.exceptions.DisambiguationError"
                    }
        return Response(json.dumps(data), mimetype='text/json')


# Main entry point for the program
api.add_resource(subject, '/api/subject/<word>')
api.add_resource(info, '/api/info')

if __name__ == '__main__':
    application.run(debug=settings.DEBUG, port=settings.PORT)
