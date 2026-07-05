from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content":"You are a helpful assistant and here to solve only mathematical related questions.If a query is other than math, just say sorry, and do not answer that"},
        {"role": "user", "content": "Hey, can you help me understanding a+b whole square?"},
    ]
)
print(response.choices[0].message.content)