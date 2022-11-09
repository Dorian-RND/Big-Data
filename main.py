import json
import spacy
from Elastic import testRecupElastic
from textblob import TextBlob

from Elastic.testRecupElastic import *

nlp = spacy.load("en_core_web_sm")

tab_polarity = []
tab_subjectivity = []


def sentiment(phrase):
    test = TextBlob(phrase)
    polarity, subjectivity = test.sentiment
    tab_polarity.append(polarity)
    tab_subjectivity.append(subjectivity)
    print("polarite -> "+ str(polarity))
    print("subjectivity -> "+ str(subjectivity))


def infoPhrase(phrase):
    test = TextBlob(phrase)
    print(test.tags)



if __name__ == '__main__':
    id = scanId("mercredimatin")
    getText("mercredimatin", id)


