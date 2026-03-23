'''
Functionality:This code implement a cahtbot using vector embeddings and use vector databsae to store and compare the similarity matching .Here only revelant chunks is sent as response to the user instead of sending the whole data + user query to model so model can geenrate new text.
trained = YES (trained based on custom given dataset)
chatbot level - Sementatic smartsearch (chatbot using vector embeddings and compare similarity matching)
tech -  embedding model(), vector database (Faiss index, pinecone, weaviate, qdrant, chroma etc) 
what you will learn -  Understand embeddings and semantic search.retrival will be learn, augment remains.
flow = database -> chunk -> embedding -> vectore db store
       userinput -> embedding -> compare with vector stored db -> top k similear chunks -> send to llm as context

extra - filtering adn reranking

'''

import requests
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer



# ------------ LOAD EMBEDDINGS ------------------
embed_model = SentenceTransformer("all-MiniLM-L6-V2") # 384 dimensions 


# ------------ LOAD CUSTOM DATA ------------------
with open("custom_dataset.txt", "r" , encoding="utf-8") as f:
    custom_data_lines = [line.strip() for line in f if line.strip()]  # remove empty lines and strip whitespace
embedded_custom_data = embed_model.encode(custom_data_lines)  # embedding the custom dataset lines
# print(f"Custom dataset loaded and embedded. Total lines: {len(custom_data_line)}\n{embedded_custom_data}")


# ------------ Make CUSTOM DATA as numpy array and Store in Vector DB ------------------
embedded_custom_data = np.array(embedded_custom_data).astype('float32')
# print(embedded_custom_data.shape)  # check the shape of the embedded data

# creating FAISS index
dimension = embedded_custom_data.shape[1]  # get the dimension of the embeddings
index = faiss.IndexFlatL2(dimension)  # create a FAISS index for L2 distance
index.add(embedded_custom_data)  # add the embedded custom data to the index
print("FAISS index created")
# faiss.write_index(index, 'custom_db.faiss')
# print(dir(index)) # check the available methods in the index


# ------------ Search Functionality  ------------------
def retrieve_context(question):
    top_k = 3  # number of top similar chunks to retrieve
    question_embedding = embed_model.encode([question]).astype("float32") # embed and convert to numpy array

    distance,indexes = index.search(question_embedding, top_k)  # search the index for similar embeddings
    print(f"DEBUG : distances: {distance}, indexes: {indexes}")

    result =[]
    for i in indexes[0]:  # indexes is a 2D array, we take the first row
        result.append(custom_data_lines[i])  # append the matched line from the custom dataset

    return result

# print(retrieve_context("what is python"))
results = retrieve_context("what is python")

print("\nTop Results:")
for r in results:
    print(r)