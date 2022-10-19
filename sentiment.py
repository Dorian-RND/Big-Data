from textblob import TextBlob
import json
from pymongo import MongoClient
import pymongo

import spacy

nlp = spacy.load("en_core_web_sm")



tab_polarity = []
tab_subjectivity = []


def sentiment(phrase):
    test = TextBlob(phrase)
    polarity, subjectivity = test.sentiment
    tab_polarity.append(polarity)
    tab_subjectivity.append(subjectivity)


def infoPhrase(phrase):
    test = TextBlob(phrase)
    print(test.tags)


# ont va lires les infos qui sont sur le serveur mongo

myclient = MongoClient("mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority")
db = myclient["BIGDATA"]
collection = db["data"]
collection.find("id")
for data in collection:
    print(data)
    print(" aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


