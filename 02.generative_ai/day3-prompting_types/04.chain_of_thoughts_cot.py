from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GENAI_API_KEY"),
    base_url=os.getenv("GENAI_BASE_URL")
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


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": "What is the output of 2+10-8/3+2?"},
        {"role":"assistant","content":json.dumps({"step": "START","content": "What is the output of 2+10-8/3+2?"})},
        {"role":"assistant","content":json.dumps({"step": "PLAN","content": "The user is asking to evaluate a mathematical expression. I need to apply the order of operations (BODMAS/PEMDAS)."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "I will first identify the operations in the expression: addition, subtraction, and division."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "According to BODMAS/PEMDAS, I will perform the division operation first: 8 / 3."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN","content": "Calculate 8 / 3, which is approximately 2.6666666666666665."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "Next, I will perform the addition and subtraction operations from left to right."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "The expression becomes 2 + 10 - 2.6666666666666665 + 2."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "Perform the addition: 2 + 10 = 12."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "Perform the subtraction: 12 - 2.6666666666666665 = 9.333333333333334."})},
        {"role":"assistant","content":json.dumps({"step": "PLAN", "content": "Perform the final addition: 9.333333333333334 + 2 = 11.333333333333334."})}
        
    ],
    temperature=0
)
print(response.choices[0].message.content)