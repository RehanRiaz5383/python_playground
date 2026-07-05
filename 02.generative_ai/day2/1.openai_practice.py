from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)
print(response.choices[0].message.content)