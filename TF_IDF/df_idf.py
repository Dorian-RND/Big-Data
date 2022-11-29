import time

from nltk import WordNetLemmatizer
from textblob import Word

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm.auto import tqdm

def df_idf(documents, fichier_idf):
    filter_docs = []
    text_tokens_lemmatize = []

    new_stopwords = [".", "n't", "?", "!", "...", ",", ";", ":", ")", "(", "&", "|", ".."]
    stopwordsCustom = stopwords.words('english')
    for new_stop in new_stopwords:
        stopwordsCustom.append(new_stop)
    time.sleep(0.5)

    lemmatizer = WordNetLemmatizer()
    print("\nTokenize")
    for doc in tqdm(documents):
        text_tokens = word_tokenize(doc.lower())
        for words_before_lemmatize in text_tokens:
            if "@" or "#" not in words_before_lemmatize :
                text_tokens_lemmatize.append(lemmatizer.lemmatize(words_before_lemmatize, pos="v"))
        filter_docs.append([word for word in text_tokens_lemmatize if not word in stopwordsCustom])
    time.sleep(0.5)

    words_set = set()
    for doc in filter_docs:
        words_set = words_set.union(doc)
    print('Nombre de mots total : ', len(words_set))
    time.sleep(0.5)

    n_docs = len(filter_docs)  # ·Number of documents in the corpus
    n_words_set = len(words_set)  # ·Number of unique words in the
    print(f"Nombre de document : {n_docs}")
    print(f"Nombre de mots uniques : {n_words_set}")
    print(words_set)

    df_tf = pd.DataFrame(np.zeros((n_docs, n_words_set)), columns=words_set)

    #print("\nCalcul DF :")
   # for i in tqdm(range(n_docs)):
     #   words = filter_docs[i]  # Words in the document
     #   for w in words:
    #        df_tf[w][i] = df_tf[w][i] + (1 / len(words))
    #time.sleep(0.5)

    print("\nCalcul IDF :")
    idf = {}
    for w in tqdm(words_set):
        k = 0  # number of documents in the corpus that contain this word
        for i in range(n_docs):
            if w in filter_docs[i]:
                k += 1
        idf[w] = np.log10(n_docs / k)
    time.sleep(0.5)

    idf = dict(sorted(idf.items(), key=lambda item: item[1]))
    print(f"\nIDF inverse :\n{idf}")

    fichier = open(fichier_idf, "w")
    fichier.write("mot;idf_inverse\n")
    for cle, valeur in idf.items():
        fichier.write(str(cle + "," + str("{:.8f}".format(valeur)) + "\n"))


