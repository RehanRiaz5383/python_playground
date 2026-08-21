#OpenAI relavent imports
from langchain_openai import OpenAIEmbeddings
#Qdrant relavent imports
from langchain_qdrant import QdrantVectorStore
#dotenv relavent imports
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

#querying from user
query = input("🤔 Please enter your query: ")

#vector embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
#vector store
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

#retrieving relevant chunks
search_results =  vector_db.similarity_search(query=query)  

#joining the context and content
context = "\n\n\n".join([f"page_content: {result.page_content}\npage_number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

#system prompt
SYSTEM_PROMPT = f"""
You are a helpful assistant that can answer user query based on the relavent context retrieved from the pdf file along with the page_content and page_number.
Use the following context to answer the user's query:
{context}

User's query: {query}

Answer the user's query based on the context provided.

If the user's query is not related to the context, say "I'm sorry, I can't answer that question."

If the user's query is related to the context, answer the question based on the context provided.

At the end of the answer, provide the source of the answer along with the page_number and file location.
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": query},
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=message_history,
)

print(response.choices[0].message.content)