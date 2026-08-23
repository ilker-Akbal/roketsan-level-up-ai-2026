import json

import pymupdf
import faiss
import numpy as np

from ollama import chat
from sentence_transformers import SentenceTransformer


# =========================================================
# CONFIG
# =========================================================

PDF_PATH = "manual.pdf"

EMBEDDING_MODEL = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

LLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"


# =========================================================
# PDF + CHUNKING
# =========================================================

def chunk_text(
    text,
    chunk_size=120,
    overlap=30,
    min_chunk_words=30
):
    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):

        chunk_words = words[
            start:start + chunk_size
        ]

        if len(chunk_words) < min_chunk_words:
            break

        chunks.append(
            " ".join(chunk_words)
        )

    return chunks


def load_pdf(pdf_path):

    pdf = pymupdf.open(pdf_path)

    documents = []

    chunk_counter = 1

    for page_number, page in enumerate(
        pdf,
        start=1
    ):
        text = page.get_text()

        chunks = chunk_text(text)

        for chunk in chunks:

            documents.append(
                {
                    "text": chunk,
                    "document": pdf_path,
                    "page": page_number,
                    "chunk_id": (
                        f"chunk_{chunk_counter:04d}"
                    )
                }
            )

            chunk_counter += 1

    return documents


# =========================================================
# VECTOR INDEX
# =========================================================

documents = load_pdf(PDF_PATH)

print("Total chunks:", len(documents))


embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


texts = [
    doc["text"]
    for doc in documents
]


embeddings = embedding_model.encode(texts)

embeddings = np.asarray(
    embeddings,
    dtype="float32"
)

faiss.normalize_L2(embeddings)


dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)


# =========================================================
# TOOL 1: RAG
# =========================================================

def rag_tool(query, top_k=5):

    query_embedding = embedding_model.encode(
        [query]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    faiss.normalize_L2(query_embedding)


    scores, indices = index.search(
        query_embedding,
        top_k
    )


    results = []


    for score, idx in zip(
        scores[0],
        indices[0]
    ):
        doc = documents[idx]

        source = (
            f"Document: {doc['document']}\n"
            f"Page: {doc['page']}\n"
            f"Chunk: {doc['chunk_id']}\n"
            f"Score: {float(score):.4f}\n"
            f"Text: {doc['text']}"
        )

        results.append(source)


    return "\n\n".join(results)


# =========================================================
# TOOL 2: CALCULATOR
# =========================================================

def calculator_tool(expression):

    allowed_chars = set(
        "0123456789.+-*/() "
    )

    if not all(
        char in allowed_chars
        for char in expression
    ):
        return "Invalid expression"

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:

        return "Calculation error"


# =========================================================
# AGENT
# =========================================================

def run_agent(user_query, max_steps=5):

    system_prompt = """
You are a technical-document AI agent.

You have two tools:

1. rag
Use this to retrieve information from the technical document.

2. calculator
Use this for arithmetic calculations.

RULES:
- Never answer document questions from memory.
- Use the rag tool when information must come from the document.
- Use the calculator tool when arithmetic is required.
- After receiving a tool result, decide whether another tool is needed.
- Do not invent document facts.
- Preserve technical numbers and units.
- Final answers must cite document/page/chunk when document information was used.
- Answer the final response in the same language as the user's question.
- When using the rag tool, send only the document search question.
- Do not include calculation or conversion instructions in the rag search query.
- Prefer concise English technical search queries for the document.
- If a retrieved result does not directly answer the document question, call the rag tool again with a more specific query.
- Do not calculate using a value unless the retrieved context clearly states that it is the value requested by the user.

On every step output ONLY valid JSON.

To call a tool:

{
  "type": "tool",
  "tool": "rag",
  "input": "search query"
}

or:

{
  "type": "tool",
  "tool": "calculator",
  "input": "177 + 273.15"
}

When finished:

{
  "type": "final",
  "answer": "final answer"
}
"""


    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_query
        }
    ]


    for step in range(1, max_steps + 1):

        response = chat(
            model=LLM_MODEL,
            messages=messages,
            options={
                "temperature": 0.0
            }
        )


        raw_output = (
            response.message.content.strip()
        )


        # JSON code fence geldiyse temizle
        raw_output = (
            raw_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


        try:
            action = json.loads(raw_output)

        except json.JSONDecodeError:

            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Invalid JSON. "
                        "Return only valid JSON."
                    )
                }
            )

            continue


        print(
            f"\n--- AGENT STEP {step} ---"
        )

        print(action)


        # =================================================
        # FINAL
        # =================================================

        if action.get("type") == "final":

            return action.get(
                "answer",
                "No answer"
            )


        # =================================================
        # TOOL CALL
        # =================================================

        if action.get("type") == "tool":

            tool_name = action.get("tool")

            tool_input = action.get("input")


            if tool_name == "rag":

                observation = rag_tool(
                    tool_input
                )


            elif tool_name == "calculator":

                observation = calculator_tool(
                    tool_input
                )


            else:

                observation = (
                    "Unknown tool"
                )


            print("\nOBSERVATION:")
            print(observation)


            # Agent'ın verdiği action'ı history'ye ekle
            messages.append(
                {
                    "role": "assistant",
                    "content": raw_output
                }
            )


            # Tool sonucunu agent'a geri ver
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "OBSERVATION:\n"
                        f"{observation}"
                    )
                }
            )


    return "Agent stopped: max steps reached."


# =========================================================
# TEST
# =========================================================

question = (
    "Dokümana göre thermal treatment sıcaklık eşiğini bul "
    "ve Celsius değerini Kelvin'e çevir."
)


answer = run_agent(question)


print("\n==============================")
print("FINAL ANSWER")
print("==============================")

print(answer)