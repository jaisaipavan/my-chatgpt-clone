from flask import Flask, request, jsonify
from flask_cors import CORS

from loader import load_data
from retriever import VectorlessRetriever
from llm import generate_answer
import os

app = Flask(__name__)
# Enable CORS for frontend origin (Vite uses 5173 or 127.0.0.1:5173, so let's allow all for now)
CORS(app)
documents = load_data()
retriever = VectorlessRetriever(documents)

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "Backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message")
    results = retriever.retrieve(user_query, top_k=3)
    context = "\n".join(results)
    answer = generate_answer(context, user_query)
    return jsonify({"response": answer})

@app.route("/upload", methods=["POST"])
def upload_file():
    files = request.files.getlist("files")
    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    global documents, retriever
    documents = load_data()
    retriever = VectorlessRetriever(documents)
    return jsonify({"status": "success", "message": f"{len(files)} files uploaded"})
if __name__ == "__main__":
    app.run(debug=True)