import os
import faiss
import torch
import pickle
from glob import glob
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# Persistent FAISS index
INDEX_FILE = "faiss_index.pkl"
DOCS_FILE = "docs.pkl"

if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "rb") as f:
        index = pickle.load(f)
    with open(DOCS_FILE, "rb") as f:
        docs = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)
    docs = []

def read_file(path):
    ext = path.split(".")[-1].lower()
    text = ""
    if ext == "pdf":
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif ext == "txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

def ingest_documents():
    global index, docs
    files = glob("data/*")
    new_docs = []
    for file in files:
        text = read_file(file)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        new_docs.extend(chunks)
    embeddings = model.encode(new_docs, convert_to_numpy=True, show_progress_bar=True)
    index.add(embeddings)
    docs.extend(new_docs)
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index, f)
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(docs, f)
    print(f"Ingested {len(new_docs)} chunks from {len(files)} files.")

def retrieve(query, top_k=3):
    q_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, top_k)
    results = [docs[i] for i in I[0]]
    return "\n\n".join(results)