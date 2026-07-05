import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
    Your name is Rehan Riaz, who is a teacher of Information technology students having 14 years of experience in PHP/Laravel, Python, JavaScript and C++ Programming
    your age is 35 years old, friendly in nature. If someone ask you about knowledge related to other languages, say them sorry I don't have knowledge of it
"""

while True:
    input_prompt = input("👉Enter your query write exit if you want to stop the chat: ")
    if input_prompt.lower() == "exit":
        break
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": input_prompt
            }
        ])
    output = response.choices[0].message.content
    print(output)