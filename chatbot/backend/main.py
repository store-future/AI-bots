from fastapi import FastAPI, UploadFile, File
from pipeline.rag_pipeline import RagPipeline
import shutil
import os

app = FastAPI()

rag = RagPipeline()



@app.get("/")
async def root_function():
    return {"message": "Fast API is working"}



UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 1️⃣ Upload + Ingest PDF
@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    rag.ingest(file_path)
    
    return {"message": "PDF processed successfully"}


# 2️⃣ Ask Question
@app.post("/ask")
async def ask_question(question: str):
    
    answer = rag.ask(question)
    
    return {
        "question": question,
        "answer": answer
    }


