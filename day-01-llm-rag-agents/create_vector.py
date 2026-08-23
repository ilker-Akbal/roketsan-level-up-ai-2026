import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from mil_std_document import MIL_STD_DOCUMENT


load_dotenv()

document = Document(
    page_content=MIL_STD_DOCUMENT,
    metadata={
        "source": "RKT-MIL-STD-001",
        "type": "technical_standard"
    }
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100
)

chunks = text_splitter.split_documents([document])

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

base_dir = Path(__file__).resolve().parent
vector_store.save_local(str(base_dir / "faiss_index"))

print(f"Toplam chunk sayısı: {len(chunks)}")
print("FAISS index oluşturuldu.")