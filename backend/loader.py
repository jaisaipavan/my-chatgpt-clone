import os
from PyPDF2 import PdfReader

DATA_DIR = "data"

def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def load_data():
    all_texts = []
    if not os.path.exists(DATA_DIR):
        return all_texts
        
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        if filename.lower().endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    all_texts.extend(chunk_text(content))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        elif filename.lower().endswith(".pdf"):
            try:
                pdf_text = ""
                reader = PdfReader(file_path)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        pdf_text += extracted + "\n"
                all_texts.extend(chunk_text(pdf_text))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return all_texts