import json

import numpy as np
from pymongo import MongoClient
from textblob import TextBlob

serveurMongo = "mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority"
nomDB = "BIGDATA"


def date(data):
    donne = []
    compteur = 0
    dateUtiliser = []
    for date in data:
        if date != None:
            compteur = 0
            jour = date.split(" ")
            if jour[0] not in dateUtiliser:
                dateUtiliser.append(jour[0])
                for data2 in data:
                    fin2=data2.split(" ")
                    if fin2[0] == jour[0]:
                        compteur += 1
                info = {
                 "date": jour[0],
                 "nb": compteur
             }
                donne.append(info)
    with open('date.json', 'w') as mon_fichier:
        json.dump(donne, mon_fichier)
    myclient = MongoClient(serveurMongo)

    db = myclient[nomDB]
    collection = db["date"]
    collection.drop()
    collection.insert_many(donne)
