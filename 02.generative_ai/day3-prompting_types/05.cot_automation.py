from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
    Your are an AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN AND OUTPUT steps.
    You need to first PLAN, what need to be done, The PLAN can be on multiple steps.
    Once you think PLAN is enough finally you can give the output
    
    Rules:
    - Strictly follow the given JSON format
    - Only run one step at a time
    - Sequence of steps is START (where user gives the input), PLAN (that can be multiple times), OUTPUT (where you give the final output)
    
    Output Format:
    {{
        "step":"String" (START, PLAN, OUTPUT),
        "content":"String" or None
    }}
    
    Example:
    START: What is the output of 2+5-3/10-2?
    PLAN: {"step":"PLAN", "content":"Seems like user is asking for a mathematical expression evaluation"}
    PLAN: {"step":"PLAN", "content":"I think this expression can be solved by BODMAS rule"}
    PLAN: {"step":"PLAN", "content":"I will first solve the division part i.e. dividing 3 by 10 which is 0.3"}
    PLAN: {"step":"PLAN", "content":"Then I will solve the addition and subtraction part i.e. 2+5-0.3-2 which is 4.7"}
    PLAN: {"step":"PLAN", "content":"The final output of the expression 2+5-3/10-2 is 4.7"},
    OUTPUT: {"step":"OUTPUT", "content":"4.7"}
"""

messages_history = [
    {"role":"system", "content":SYSTEM_PROMPT},
]

prompt = input("👉Enter your query: ")
messages_history.append({"role": "user", "content": prompt})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type":"json_object"},
        messages=messages_history   
    )
    raw_response = response.choices[0].message.content
    messages_history.append({"role": "assistant", "content": raw_response})
    json_response = json.loads(raw_response)
    if json_response.get("step") == "START":
        print(f"🔥 {json_response.get("content")}")
        continue
    if json_response.get("step") == "PLAN":
        print(f"🤖 {json_response.get("content")}")
        continue
    if json_response.get("step") == "OUTPUT":
        print(f"✅ {json_response.get("content")}")
        break

