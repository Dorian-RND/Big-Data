#  TOPIC MODELING/TEXT CLASS. SERIES  #
#             Lesson 02.03            #
# TF-IDF in Python with Scikit Learn  #
#               with                  #
#        Dr. W.J.B. Mattingly         #
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import string
from nltk.corpus import stopwords
import json
import glob
import re
import nltk
nltk.download('stopwords')


docs = [
    "RedBull gives U F1xed Wings Mfs AustinGP",
    "SilverArrowsNet Exact same wording as Max. Staged",
    "cytrusf1 MBS doesn't deserve to be F1 president he's a bad leader with zero personality Hamilton",
    "Redbull gives U F1xed Wings Mfs",
    "Redbull as Max",
    "Redbull F1 Horner Max Staged.",
    "Mercedes Hamilton",
]


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


def clean_docs(docs):
    stops = stopwords.words("english")
    final = []
    for doc in docs:
        clean_doc = remove_stops(doc, stops)
        final.append(clean_doc)
    return (final)


descriptions = docs

# print (descriptions[0])

cleaned_docs = clean_docs(descriptions)
# print (cleaned_docs[0])

vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=100,
#    max_df=0.8,
#    min_df=5,
    ngram_range=(1, 3),
    stop_words="english"

)

vectors = vectorizer.fit_transform(cleaned_docs)

feature_names = vectorizer.get_feature_names()

dense = vectors.todense()
denselist = dense.tolist()

all_keywords = []

for description in denselist:
    x = 0
    keywords = []
    for word in description:
        if word > 0:
            keywords.append(feature_names[x])
        x = x + 1
    all_keywords.append(keywords)
print(descriptions[0])
print(all_keywords[0])

true_k = 3

model = KMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)

model.fit(vectors)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

with open("clustering_textes.csv", "w", encoding="utf-8") as f:
    f.write("cluster;mot\n")
    for i in range(true_k):
        for ind in order_centroids[i, :10]:
            f.write(f"Cluster_{i};")
            f.write('%s' % terms[ind], )
            f.write("\n")