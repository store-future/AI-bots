from ingestion.pdf_loader import load_pdf
from core.chunking import chunk_text
from core.embeddings import EmbeddingModel
from core.vector_store import VectorStore
from core.llm import LLMClient


class RagPipeline:

    def __init__(self):
        self.embedder = EmbeddingModel()
        self.llm = LLMClient(
            model="google/gemma-3-4b",
            url="http://localhost:1234/api/v1/chat"
        )
        self.vector_store = None
        
    
    def ingest(self,filepath):
        text = load_pdf(filepath)
        chunks = chunk_text(text)
        embeddings = self.embedder.encode(chunks)

        dim = len(embeddings[0])
        self.vector_store = VectorStore(dim)
        self.vector_store.add(embeddings,chunks)
        
    
    def ask(self,question):
        q_vec = self.embedder.encode([question])

        context = self.vector_store.search(q_vec)
        prompt = f"""
        You are an intelligent assistant.

        You are given some context from a document.

        Your job:
        - If the context is relevant, use it to answer
        - If the context is NOT relevant, ignore it and answer normally
        - Do NOT say "I don't know" unless truly necessary

        Give a clear, human-friendly answer.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        return self.llm.generate(prompt)



# rag = RagPipeline()
# filepath = "data/uploads/Dhananjay_Resume (2) (1).pdf"
# rag.ingest(filepath)
# # print(rag.ask("what is the  mobile no and name of this resume person"))

# while True :
    
#     print(rag.ask(input("ask")))
