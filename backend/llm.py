from groq import Groq

# Set your GROQ_API_KEY in environment variables
import os
api_key = os.environ.get("gsk_2h8wXz224Wd1pQ9h8wXz224Wd1pQ9h8w")
client = Groq(api_key=api_key)

def generate_answer(context, user_query):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {user_query}"}
        ]
    )
    return response.choices[0].message.content