from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Hello, how are you?"
)
print(interaction.output_text)