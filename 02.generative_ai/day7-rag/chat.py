from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
#Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")


#Connecting vector db i.e. Qdrant and indexing chunks
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)


query = input("Enter your query: ")

#similarity search user query in vector db
#this will return relavent chunks from vector db
search_results =  vector_db.similarity_search(query=query)  

#joining the context and content
context = "\n\n\n".join([f"page_content: {result.page_content}\npage_number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
You are a helpful assistant that can answer user query based on the relavent context retrieved from the pdf file along with the page_content and page_number.
You should only answer the question based on the following context and nevigate the user to open the pdf file and read the context from the page_content and page_number and navigate the user to open page number and know more.
Context: {context}
"""

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

messages_history = [
            {"role":"system", "content":SYSTEM_PROMPT},
]

messages_history.append({"role": "user", "content": query})

response = client.chat.completions.create(
    model="gpt-5",
    messages=messages_history
)

print(f"🤖 Assistant: {response.choices[0].message.content}")