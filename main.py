import json
import spacy

nlp = spacy.load("en_core_web_sm")
from pymongo import MongoClient
from textblob import TextBlob

serveurMongo = "mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority"
nomDB = "BIGDATA"
nomCollection = "data"
fichierJson = 'data_19-10-2022.json'

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


def suppressionMotVide(phrase):
    doc = nlp(phrase)
    # Analyze syntax
    print(" phrase -> " + result.get("text"))
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
    for entity in doc.ents:
        print(entity.text, entity.label_)


if __name__ == '__main__':

    # Making Connection
    myclient = MongoClient(serveurMongo)

    # database
    db = myclient[nomDB]

    # reset de la collection
    collection = db[nomCollection]
    collection.drop()
    collection = db[nomCollection]

    with open(fichierJson) as file:
        file_data = json.load(file)
    print(file_data)

    # ajout dans la BDD
    if isinstance(file_data, list):
        collection.insert_many(file_data)
    else:
        collection.insert_one(file_data)
    print("donnée send")



    donnees = collection.find()
    for result in donnees:

        suppressionMotVide(result.get("text"))
        # TODO mettres les sentiments
