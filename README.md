# PyumIpsum
PyumIpsum is a keyword/content aware LoremIpsum generator. You supply a word and it'll generate a randomly generator human readable sentence for you. You can also supply a seed word so that the content is not only based on a subject, but can also be seeded with a word you specify.

## Tech Used:

* [Markov Generator](https://github.com/TehMillhouse/PyMarkovChain)- I use this to actually generate the sentences. As I better myself in Markov Chains, and language processing, I expect this algorithim to improve.
* [Python Natural Language ToolKit](http://www.nltk.org/)- I'll be using this as another way of generating sentences among other things. Word counts, tokenizations, and word frequency.
* [Flask](http://flask.pocoo.org/)- I'm using Flask to power the REST endpoints and the site itself.


## TO-DO

1. **Create a caching mechanism**- Once a model is generated, save the pickled model to a cache. This will allow us to not having to scrape sample-content every time a request comes through.
2. **Common word count**- Use NLTK to get a list of the top 3(or 5) most commonly used words (other than stop words) in a given sample content. This could be added to the sample content for a single word and can also help in pre-generating models.