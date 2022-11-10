import time
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm.auto import tqdm
import math

docs = [
    "RedBull gives U F1xed Wings Mfs AustinGP",
    "SilverArrowsNet Exact same wording as Max. Staged",
    "cytrusf1 MBS doesn't deserve to be F1 president he's a bad leader with zero personality Hamilton",
    "Redbull gives U F1xed Wings Mfs",
    "Redbull as Max",
    "Redbull F1 Horner Max Staged.",
    "Mercedes Hamilton",
]


def df_idf(documents, fichier_idf):
    filter_docs = []

    for doc in documents:
        text_tokens = word_tokenize(doc.lower())
        filter_docs.append([word for word in text_tokens if not word in stopwords.words('english')])

    words_set = set()
    for doc in filter_docs:
        words_set = words_set.union(doc)
    print('Nombre de mots total : ', len(words_set))

    n_docs = len(filter_docs)  # ·Number of documents in the corpus
    n_words_set = len(words_set)  # ·Number of unique words in the
    print(f"Nombre de document : {n_docs}")
    print(f"Nombre de mots uniques : {n_words_set}")

    df_tf = pd.DataFrame(np.zeros((n_docs, n_words_set)), columns=words_set)

    print("\nCalcul DF :")
    for i in tqdm(range(n_docs)):
        words = filter_docs[i]  # Words in the document
        for w in words:
            df_tf[w][i] = df_tf[w][i] + (1 / len(words))

    print("\nCalcul IDF :")
    idf = {}
    for w in tqdm(words_set):
        k = 0  # number of documents in the corpus that contain this word
        for i in range(n_docs):
            if w in filter_docs[i]:
                k += 1
        idf[w] = np.log10(n_docs / k)

    idf = dict(sorted(idf.items(), key=lambda item: item[1]))
    print(f"\nIDF inverse :\n{idf}")

    fichier = open(fichier_idf, "w")
    fichier.write("mot;idf_inverse\n")
    for cle, valeur in idf.items():
        fichier.write(str(cle + ";" + str(valeur) + "\n"))


df_idf(docs, "idf_save.csv")