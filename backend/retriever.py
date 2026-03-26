from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class VectorlessRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.doc_vectors = self.vectorizer.fit_transform(documents)

    def retrieve(self, query, top_k=3):
        query_vec = self.vectorizer.transform([query])
        scores = (self.doc_vectors @ query_vec.T).toarray().flatten()

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [self.documents[i] for i in top_indices]