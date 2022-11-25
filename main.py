import json
import spacy

from Sentiment.Sentiment import sentiment

nlp = spacy.load("en_core_web_sm")
from pymongo import MongoClient

serveurMongo = "mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority"
nomDB = "BIGDATA"
nomCollection = "data"
fichierJson = "dataRecup.json"

tab_polarity = []
tab_subjectivity = []

def cluster(db):
    collection = db["cluster"]
    collection.drop()
    with open('cluster.json', 'r') as f:
        data = json.load(f)
    print(data)
    cluster0 = {
        "nomCluster": "cluster 0",
        "donnee": data[0]["0"]
    }
    cluster1 = {
        "nomCluster": "cluster 1",
        "donnee": data[0]["1"]
    }
    cluster2 = {
        "nomCluster": "cluster 2",
        "donnee": data[0]["2"]
    }
    cluster3 = {
        "nomCluster": "cluster 3",
        "donnee": data[0]["3"]
    }
    collection.insert_one(cluster0)
    collection.insert_one(cluster1)
    collection.insert_one(cluster2)
    collection.insert_one(cluster3)


def insererdoc():
    collection = db[nomCollection]
    #collection.drop()
    with open(fichierJson) as file:
        file_data = json.load(file)
    # ajout dans la BDD
    collection.insert_many(file_data)


if __name__ == '__main__':
    text=[]
    # Making Connection
    myclient = MongoClient(serveurMongo)
    print("connecter")
    # database
    db = myclient[nomDB]
    collection = db[nomCollection]
    #insererdoc()

    # pour inserer les sentiments
   # donnees = collection.find()
    #for result in donnees:
    #    text.append(result.get("text"))
    #sentiment(text)
    cluster(db)
