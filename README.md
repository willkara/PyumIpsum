# PyumIpsum
PyumIpsum is a keyword/content aware LoremIpsum generator. You supply a word and it'll generate a randomly generator human readable sentence for you. You can also supply a seed word so that the content is not only based on a subject, but can also be seeded with a word you specify.

I will be setting up a demo website and offical API site shortly.

## Tech Used:

* [Markov Generator](https://github.com/TehMillhouse/PyMarkovChain)- I use this to actually generate the sentences. As I better myself in Markov Chains, and language processing, I expect this algorithim to improve.
* [Python Natural Language ToolKit](http://www.nltk.org/)- I'll be using this as another way of generating sentences among other things. Word counts, tokenizations, and word frequency.
* [Flask](http://flask.pocoo.org/)- I'm using Flask to power the REST endpoints and the site itself.


## TO-DO

1. Extend the `saving` of models to a SQLite database. This should allow models to be able to be saved isntead of just in memory.
2. Research possibility of other scrapers.
3. Setup demo site and official API site.