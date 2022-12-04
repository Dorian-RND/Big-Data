import json
import re
import string

import pandas as pd
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
#  TOPIC MODELING/TEXT CLASS. SERIES  #
#             Lesson 02.03            #
# TF-IDF in Python with Scikit Learn  #
#               with                  #
#        Dr. W.J.B. Mattingly         #
from sklearn.feature_extraction.text import TfidfVectorizer

from Sentiment.Sentiment import sentiment
from TF_IDF.Nouvelle_Version.df_idfV2 import calc_df_idfV2
from collectTweet.CSVtoJSON import csv_to_json
from date.date import date
from pays.pays import recherchePays

nlp = spacy.load("en_core_web_sm")
from pymongo import MongoClient

serveurMongo = "mongodb+srv://bigData:comptedevfac72@cluster0.ot9fmac.mongodb.net/?retryWrites=true&w=majority"
nomDB = "BIGDATA"
nomCollection = "data"
fichierJson = "dataRecup.json"

tab_polarity = []
tab_subjectivity = []


def remove_stops(text, stops):
    text = re.sub(r"AC\/\d{1,4}\/\d{1,4}", "", text)
    words = text.split()
    final = []
    for word in words:
        if word not in stops:
            final.append(word)
    final = " ".join(final)
    final = final.translate(str.maketrans("", "", string.punctuation))
    final = "".join([i for i in final if not i.isdigit()])
    while "  " in final:
        final = final.replace("  ", " ")
    return (final)


def lemmatize_docs(doc):
    word_list = word_tokenize(doc)

    lemmatizer = WordNetLemmatizer()
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w, pos="v") for w in word_list])
    return lemmatized_output


def clean_docs(docs):
    new_stopwords = [".", "n't", "?", "!", "...", ",", ";", ":", ")", "(", "&", "|", "..", "red", "bull", "redbull"]
    stopwordsCustom = stopwords.words('english')
    for new_stop in new_stopwords:
        stopwordsCustom.append(new_stop)
    final = []
    for doc in docs:
        doc = doc.lower()
        clean_doc = remove_stops(lemmatize_docs(doc), stopwordsCustom)

        clean_doc = clean_doc.replace("redbull", "")
        clean_doc = clean_doc.replace("red", "")
        clean_doc = clean_doc.replace("bull", "")
        print(clean_doc)

        final.append(clean_doc)
    return final


def clustering(donnees):
    # print (descriptions[0])
    print("Début cleanDoc\n")
    cleaned_docs = clean_docs(donnees)

    print("Début tfIdf\n")
    vectorizer = TfidfVectorizer(lowercase=True, min_df=int((len(donnees) / 100) * 2), max_df=0.8, ngram_range=(1, 1),
                                 stop_words='english',
                                 use_idf=True)
    print("Fin tfIdf\n")
    print("Début fit_transform\n")
    # X = vectorizer.fit_transform(cleaned_docs)
    print(cleaned_docs)
    X = vectorizer.fit_transform(cleaned_docs)
    true_k = 4
    print("KMeans\n")
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    dictCluster = dict()
    for i in range(true_k):
        dictCluster[i] = []
    for i in range(true_k):
        print(f"Cluster {i}: ", end="")
        for ind in order_centroids[i, :6]:
            dictCluster[i].append(terms[ind])
            print(f"{terms[ind]}, ", end="")
        print()
    print(dictCluster)
    jsonString = json.dumps(dictCluster)
    jsonFile = open("cluster.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def cluster(db):
    collection = db["cluster"]
    collection.drop()
    with open('cluster.json', 'r') as f:
        data = json.load(f)
    print(data)
    cluster0 = {
        "nomCluster": "cluster 0",
        "donnee": data["0"]
    }
    cluster1 = {
        "nomCluster": "cluster 1",
        "donnee": data["1"]
    }
    cluster2 = {
        "nomCluster": "cluster 2",
        "donnee": data["2"]
    }
    cluster3 = {
        "nomCluster": "cluster 3",
        "donnee": data["3"]
    }
    collection.insert_one(cluster0)
    collection.insert_one(cluster1)
    collection.insert_one(cluster2)
    collection.insert_one(cluster3)


def insererdoc():
    collection = db[nomCollection]
    collection.drop()
    with open(fichierJson) as file:
        file_data = json.load(file)
    # ajout dans la BDD
    collection.insert_many(file_data)


def maxlike(like, text, db):
    collection = db["like"]
    collection.drop()
    p = []
    none = 0
    for i in like:
        if i is None:
            none = none + 1
        else:

            p.append(i)
    yes = p.index(max(p))
    print(like[yes])
    like = {
        "nblike": str(like[yes]),
        "texte": text[yes]
    }

    collection.insert_one(like)


def maxRT(rt, text, db):
    collection = db["rt"]
    collection.drop()
    p = []
    none = 0
    for i in rt:
        if i is None:
            none = none + 1
        else:

            p.append(i)
    yes = p.index(max(p))
    like = {
        "nblike": str(rt[yes]),
        "texte": text[yes]
    }

    collection.insert_one(like)


if __name__ == '__main__':
    text = []
    pays = []
    rt = []
    like = []
    datetweet = []
    # Making Connection
    myclient = MongoClient(serveurMongo)
    print("connecter")
    # database
    db = myclient[nomDB]
    collection = db[nomCollection]
    # insererdoc()
    # pour inserer les sentiments
    donnees = collection.find()
    for result in donnees:
        if result.get("tweet_localisation") is not None:
            text.append(result.get("tweet_localisation"))
            like.append(result.get("nb_Like"))
            rt.append(result.get("nb_RT"))
        pays.append(result.get("tweet_text"))
        datetweet.append(result.get("tweet_date"))

    # sentiment(text)
    # recherchePays(pays)
    # clustering(text)
    # cluster(db)
    # date(datetweet)
    # maxlike(like, text, db)
    # maxRT(rt, text, db)



    tfIdfVectorizer = TfidfVectorizer(use_idf=True)
    tfIdf = tfIdfVectorizer.fit_transform(text)
    df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)
    var=df.head(10)
    index=var.index
    values=var.values
    l=[]
    m=[]
    for i in index:
        l.append(i)
    for k in values:
        m.append(k[0])
    ins=[]
    collection = db["tfidf"]
    collection.drop()
    for s in range(len(m)):



        like = {
            "mot": l[s],
            "nombre": str(m[s])
        }
        ins.append(like)

    collection.insert_many(ins)

