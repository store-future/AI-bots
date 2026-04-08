import faiss
import numpy as np


class VectorStore:

    def __init__(self,dim):
        self.index = faiss.IndexFlatL2(dim) 
        self.texts = []

    def add(self,embeddings,texts):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.texts.extend(texts)
        
    def search(self,query_embedding, k=3):
        query_embedding = np.array(query_embedding).astype('float32')

        distance, indices = self.index.search(query_embedding,k)

        context =[]
        for i in indices[0]:
            context.append(self.texts[i])
        
        return context

    def save(self):
        pass