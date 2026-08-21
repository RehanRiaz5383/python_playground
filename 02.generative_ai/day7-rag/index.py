from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()
#loading docs to memory
filepath = Path(__file__).parent / "doc.pdf"
loader = PyPDFLoader(file_path=filepath)
docs = loader.load()



#splitting docs into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(docs)

#Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

#Connecting vector db i.e. Qdrant and indexing chunks
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

print("Vector embeddings of docs done")