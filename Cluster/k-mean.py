#  TOPIC MODELING/TEXT CLASS. SERIES  #
#             Lesson 02.03            #
# TF-IDF in Python with Scikit Learn  #
#               with                  #
#        Dr. W.J.B. Mattingly         #
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import string
from nltk.corpus import stopwords
import json
import glob
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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
    new_stopwords = [".", "n't", "?", "!", "...", ",", ";", ":", ")", "(", "&", "|", ".."]
    stopwordsCustom = stopwords.words('english')
    for new_stop in new_stopwords:
        stopwordsCustom.append(new_stop)
    final = []
    for doc in docs:
        clean_doc = remove_stops(lemmatize_docs(doc), stopwordsCustom)
        final.append(clean_doc)
    return (final)


def clustering(donnees):
    # print (descriptions[0])
    print("Début cleanDoc\n")
    cleaned_docs = clean_docs(donnees)


    print("Début tfIdf\n")
    vectorizer = TfidfVectorizer(lowercase=True, min_df=6, max_df=0.8, ngram_range=(1,1), stop_words='english', use_idf=True)
    print("Fin tfIdf\n")
    print("Début fit_transform\n")
    #X = vectorizer.fit_transform(cleaned_docs)
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


