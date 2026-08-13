from ollama import Client
from fastapi import FastAPI, Body


app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def load_chat(message:str = Body(...,description="The message")):
    response = client.chat(model="qwen3.5:0.8b",messages = [
        {"role":"user","content":message}
    ])
    return {"response":response.message.content}