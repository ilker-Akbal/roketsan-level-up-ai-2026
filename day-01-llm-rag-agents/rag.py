import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


# create_vector.py'de kullandığın embedding modeliyle aynı olmalı
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


base_dir = Path(__file__).resolve().parent

vector_store = FAISS.load_local(
    str(base_dir / "faiss_index"),
    embeddings,
    allow_dangerous_deserialization=True
)


retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Sen teknik döküman sorularını cevaplayan bir asistansın.

            Kullanıcının sorusunu sadece sana verilen context
            içerisindeki bilgileri kullanarak cevapla.

            Context içinde cevap bulunmuyorsa:
            "Bu bilgi dökümanda bulunmuyor."
            şeklinde cevap ver.
            """
        ),

        (
            "human",
            """
            CONTEXT:
            {context}

            SORU:
            {question}
            """
        )
    ]
)


out_parser = StrOutputParser()

chain = prompt | model | out_parser


question = "Elektronik kontrol biriminin maksimum çalışma sıcaklığı nedir?"


documents = retriever.invoke(question)


context = "\n\n".join(
    document.page_content
    for document in documents
)


response = chain.invoke(
    {
        "context": context,
        "question": question
    }
)


print(response)