import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# 1. Initialize the client with the Hugging Face router base URL
# and your Hugging Face User Access Token (starts with hf_...)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")  # Or paste your string token directly
)

# 2. Call the chat completion endpoint
# Use the Hugging Face repo ID as the model name (e.g., "meta-llama/Llama-3.1-8B-Instruct")
response = client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B-Instruct-2507",
    messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": "Hey, How are you?"}
    ],
    max_tokens=100
)

# 3. Print the output just like you would with OpenAI
print(response.choices[0].message.content)