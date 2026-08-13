from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json


load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return null

SYSTEM_PROMPT = """
    Your are an AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN AND OUTPUT steps.
    You need to first PLAN, what need to be done, The PLAN can be on multiple steps.
    You can also call the tool from the list of available tools if required.
    For every tool called, wait for the observe step which is the output for every tool called
    Once you think PLAN is enough finally you can give the output
    
    Rules:
    - Strictly follow the given JSON format
    - Only run one step at a time
    - Sequence of steps is START (where user gives the input), PLAN (that can be multiple times), OUTPUT (where you give the final output)
    
    Tools:
    - get_weather(city:str) = Takes the city as an input parameter and return the weather information about that city
    
    Output JSON Formats depending on the step:

    1. For a PLAN step:
    {
        "step": "PLAN",
        "content": "Your reasoning or plan details go here"
    }

    2. For a TOOL call step (when you need to use a tool):
    {
        "step": "TOOL",
        "tool": "get_weather",
        "input": "city_name"
    }

    3. For the final OUTPUT step (when you have the final answer):
    {
        "step": "OUTPUT",
        "content": "The final response to the user goes here"
    }
    
    Example 1:
    START: What is the output of 2+5-3/10-2?
    PLAN: {"step":"PLAN", "content":"Seems like user is asking for a mathematical expression evaluation"}
    PLAN: {"step":"PLAN", "content":"I think this expression can be solved by BODMAS rule"}
    PLAN: {"step":"PLAN", "content":"I will first solve the division part i.e. dividing 3 by 10 which is 0.3"}
    PLAN: {"step":"PLAN", "content":"Then I will solve the addition and subtraction part i.e. 2+5-0.3-2 which is 4.7"}
    PLAN: {"step":"PLAN", "content":"The final output of the expression 2+5-3/10-2 is 4.7"},
    OUTPUT: {"step":"OUTPUT", "content":"4.7"}
    
    Example 2:
    START: What is the weather in Lahore?
    PLAN: {"step":"PLAN", "content":"Seems like user is asking for current weather in Lahore"}
    PLAN: {"step":"PLAN", "content":"Great, we have get_weather tool available for this query."}
    PLAN: {"step":"PLAN", "content":"I need to call get_weather tool for Lahore as the input"}
    PLAN: {"step":"TOOL", "tool":get_weather, "input":"Lahore"}
    PLAN: {"step":"OBSERVER","tool":get_weather,"input":"Lahore", "output":"The Temperature of Lahore is 30C with Cloudy Weather"}
    PLAN: {"step":"PLAN", "content":"Great, I get the weather info about Lahore"}
    PLAN: {"step":"PLAN", "content":"I need to call get_weather tool for Lahore as the input"}
    OUTPUT: {"step":"OUTPUT", "content":"The Current Temperature of Lahore is 30C with Cloudy Weather"}
    
"""

available_tools = {
    "get_weather":get_weather
}



messages_history = [
    {"role":"system", "content":SYSTEM_PROMPT},
]



def main():
    query = input("🤔 Please enter your query: ")
    messages_history.append({"role": "user", "content": query})
    while True:
        response = client.chat.completions.create(
            model="Qwen/Qwen3-235B-A22B-Instruct-2507",
            response_format={"type":"json_object"},
            messages=messages_history   
        )
        raw_response = response.choices[0].message.content
        messages_history.append({"role": "assistant", "content": raw_response})
        json_response = json.loads(raw_response)
        if json_response.get("step") == "START":
            print(f"🔥 {json_response.get("content")}")
            continue
        if json_response.get("step") == "TOOL":
            tool_called = json_response.get("tool")
            tool_input = json_response.get("input")
            print(f"🔨 Calling tool {tool_called}({tool_input})")
            response = available_tools[tool_called](tool_input)
            messages_history.append({"role":"developer","content":json.dumps({
                "step":"OBSERVE",
                "tool":tool_called,
                "input":tool_input,
                "output":response
            })})
            continue
        if json_response.get("step") == "PLAN":
            print(f"🤖 {json_response.get("content")}")
            continue
        if json_response.get("step") == "OUTPUT":
            print(f"✅ {json_response.get("content")}")
            break


main()