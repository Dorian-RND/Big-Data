import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

docs = ["the house had a tiny little mouse",
        "the cat saw the mouse",
        "the mouse ran away from the house",
        "the cat finally ate the mouse",
        "the end of the mouse story"]

tfidf_vectorizer = TfidfVectorizer(input=docs, stop_words='english')

tfidf_vector = tfidf_vectorizer.fit_transform(docs)

tfidf_df = pd.DataFrame(tfidf_vector.toarray(), columns=tfidf_vectorizer.get_feature_names())

tfidf_df.loc['Document Frequency'] = (tfidf_df > 0).sum()

tfidf_slice = tfidf_df[['mouse', 'house', 'cat']]

print(tfidf_slice)
