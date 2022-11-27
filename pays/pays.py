import json

import numpy as np
from pymongo import MongoClient
from textblob import TextBlob

serveurMongo = "mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority"
nomDB = "BIGDATA"


def recherchePays(data):
    donne = []

    for pays in data:

        if pays != None:
            print(pays)
            info = {
                "pays": pays
            }

            donne.append(info)

    with open('pays.json', 'w') as mon_fichier:
        json.dump(donne, mon_fichier)
    myclient = MongoClient(serveurMongo)

    db = myclient[nomDB]
    collection = db["pays"]
    collection.drop()
    collection.insert_many(donne)
