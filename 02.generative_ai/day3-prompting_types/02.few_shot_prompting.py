from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GENAI_API_KEY"),
    base_url=os.getenv("GENAI_BASE_URL")
)

#FEW SHOT PROMPT - Provides the model with a few examples of the desired output format before presenting the actual task. In real world, few shot prompting is used to provide the model with a few examples of the desired output format before presenting the actual task. This helps the model understand the context and produce more accurate responses. and it produce accuracy of result up to 50X
SYSTEM_PROMPT = """
You are a helpful assistant and here to solve only coding related questions. If a query is other than coding, just say sorry.

Example 1:
User: Can you write a Python function to calculate the factorial of a number?
Assistant: def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
        
Example 2:
User: How do I reverse a string in Python?
Assistant: def reverse_string(s):
    return s[::-1]
    
Example 3:
User: Can you explain a+b whole square?
Assistant: Sorry! I can only help with coding related questions. Please ask a coding question.

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": "Can you please explain (a+b)^2?"},
    ]
)
print(response.choices[0].message.content)