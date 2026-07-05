from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GENAI_API_KEY"),
    base_url=os.getenv("GENAI_BASE_URL")
)

#ZERO SHOT PROMPT - STRAIGHT FORWARD TO THE POINT PROMPTING
SYSTEM_PROMPT = "You are a helpful assistant and here to solve only coding related questions.If a query is other than coding, just say sorry"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, can you write a short program in python that print hello world?"},
    ]
)
print(response.choices[0].message.content)