import requests

try:
    res = requests.post(
        "http://127.0.0.1:5000/chat",
        json={"message": "What is RAG?"}
    )

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.json())

except Exception as e:
    print("ERROR:", e)