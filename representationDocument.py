import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

docs = ["the house had a tiny little mouse",
        "the cat saw the mouse",
        "the mouse ran away from the house",
        "the cat finally ate the mouse",
        "the end of the mouse story"]

# instantiate CountVectorizer()
cv = CountVectorizer()

# this steps generates word counts for the words in your docs
word_count_vector = cv.fit_transform(docs)

print(f"Shape : {word_count_vector.shape}")

# IDF VALUES
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)
# print idf values
df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(), columns=["idf_weights"])
# sort ascending
df_idf = df_idf.sort_values(by=['idf_weights'])
print(df_idf)

# TF-IFD VALUES
# count matrix
count_vector = cv.transform(docs)
# tf-idf scores
tf_idf_vector = tfidf_transformer.transform(count_vector)

feature_names = cv.get_feature_names()
# get tfidf vector for first document
first_document_vector = tf_idf_vector[0]
# print the scores
df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
df = df.sort_values(by=["tfidf"], ascending=False)
print(df)