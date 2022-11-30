import json

import numpy as np
from pymongo import MongoClient
from textblob import TextBlob

tab_polarity = []
tab_subjectivity = []

serveurMongo = "mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority"
nomDB = "BIGDATA"


def ecriture(polarity, subjectivity):
    donne = []
    for polarite in (polarity):
        polarite = float(polarite)
        if polarite < -0.5:
            polarite = "tres negatif"
        elif -0.5 <= polarite < 0.0:
            polarite = "negatif"
        elif polarite == 0.0:
            polarite = "neutre"
        elif 0.0 < polarite < 0.5:
            polarite = "positif"
        else:
            polarite = "tres positif"

        for j in subjectivity:
            subjectivite = j

        info = {
            "sentiment": polarite
        }
        donne.append(info)

    with open('sentiment.json', 'w') as mon_fichier:
        json.dump(donne, mon_fichier)
    myclient = MongoClient(serveurMongo)

    db = myclient[nomDB]
    collection = db["sentiment"]
    collection.drop()

    collection.insert_many(donne)


def sentiment(donnee):
    for i in donnee:
        if i is not None:
            test = TextBlob(i)
            polarity, subjectivity = test.sentiment
            tab_polarity.append(polarity)
            tab_subjectivity.append(subjectivity)
    ecriture(tab_polarity, tab_subjectivity)
