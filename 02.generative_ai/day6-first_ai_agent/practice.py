from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return FALSE  


def initiate_ai():
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    SYSTEM_PROMPT = """
        You are an AI Assistent and helping here to solve any kind of query
        Your work is on START, PLAN, TOOL, OBSERVE, OUTPUT steps
        You need to first PLAN, what need to be done, planning can be in multiple steps.
        You can call the tool from available list of tools if required
        For every tool called, wait for the OBSERVE step, that is actually the output from the tool.
        Once your plan is enough, you can finally give the OUTPUT.
        
        Rules:
        - Strictly follow the given json OUTPUT for every step
            a) For PLAN step
                {"step","PLAN", "content":"any content explaining your plan"}
            b) FOR TOOL step
                {"step":"TOOL","tool":"get_weather","input":"lahore"}
            c) FOR OBSERVE step
                {"step":"OBSERVE","tool":"get_weather","input":"lahore",output:"Haze +45°C"}
            c) FOR OUTPUT step
                {"step":"OUTPUT","content":"output received from the tool in observe step, or automatic generated output if tool not used"}
        
        EXAMPLE 1:
            START: WHAT is the output of 2+2?
            PLAN: {"step":"PLAN","content":"User is trying to get output of a mathematical question"}
            PLAN: {"step":"PLAN","content":"It is simple arithmetic question of addition"}
            OUTPUT: {"step":"OUTPUT","content":"The output of 2+2 is 4"}
        EXAMPLE 2:
            START: What is the weather now in Lahore?
            PLAN: {"step":"PLAN","content":"Looks like user wants to get weather information"}
            PLAN: {"step":"PLAN","content":"Since I don't have the appropriate real time knowledge of weather but I can check if there is a tool available for it"}
            PLAN: {"step":"PLAN","content":"Checking available tools, Great get_weather is available as weather tool."}
            TOOL: {"step":"TOOL","tool":"get_weather","input":"Lahore"}
            OBSERVE:{"step":"OBSERVE","tool":"get_weather","input":"Lahore","output":"The weather in Lahore is Haze +45°C"}
            PLAN:{"step":"PLAN","content":"Finally get the weather information now ready to display the output"}
            OUTPUT: {"step":"OUTPUT","content":"The weather in Gujranwala is Haze +45°C"}
    """
    messages_history = []
    while True:
        messages_history = []
        answer = input("👉 Please enter your query: ")
        messages_history.append({"role":"system","content":SYSTEM_PROMPT})
        messages_history.append({"role": "user", "content": answer})
        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type":"json_object"},
                messages=messages_history   
            )
            raw_response = response.choices[0].message.content
            

#main process
if __name__ == "__main__":
   