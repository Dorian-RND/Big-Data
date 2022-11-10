import spacy
from Elastic.testRecupElastic import *
from Sentiment.Sentiment import *

nlp = spacy.load("en_core_web_sm")


def infoPhrase(phrase):
    test = TextBlob(phrase)
    print(test.tags)


if __name__ == '__main__':
    id = scanId("mercredimatin")
    getText("mercredimatin", id)
    print(contenuTweet)
    sentiment(contenuTweet)
