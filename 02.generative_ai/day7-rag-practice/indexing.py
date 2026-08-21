"""
Relavent imports
"""
#pdf library
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
#chunking libraries
from langchain_text_splitters import RecursiveCharacterTextSplitter
#vector embeddings
from langchain_openai import OpenAIEmbeddings
#vector store
from langchain_qdrant import QdrantVectorStore

load_dotenv()

#loading docs to memory
filepath = Path(__file__).parent / "doc.pdf"
loader = PyPDFLoader(file_path=filepath)
docs = loader.load()


#splitting docs into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(docs)

#vector embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_db = QdrantVectorStore.from_documents(

    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

print("Indexing complete")



