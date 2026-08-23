import pymupdf
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


PDF_PATH = "manual.pdf"


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

        end = start + chunk_size

        chunk_words = words[start:end]

        if len(chunk_words) < min_chunk_words:
            break

        chunk = " ".join(chunk_words)

        chunks.append(chunk)

    return chunks


def load_pdf(pdf_path):

    pdf = pymupdf.open(pdf_path)

    documents = []

    chunk_counter = 1

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text()

        chunks = chunk_text(text)

        for chunk in chunks:

            documents.append(
                {
                    "text": chunk,
                    "document": pdf_path,
                    "page": page_number,
                    "chunk_id": f"chunk_{chunk_counter:04d}"
                }
            )

            chunk_counter += 1

    return documents


# PDF → chunks + metadata
documents = load_pdf(PDF_PATH)

print("Total chunks:", len(documents))


# Embedding model
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# Chunk textlerini çıkar
texts = [doc["text"] for doc in documents]


# Chunk → Embeddings
document_embeddings = model.encode(texts)

document_embeddings = np.asarray(
    document_embeddings,
    dtype="float32"
)


# Cosine similarity için normalize
faiss.normalize_L2(document_embeddings)


# FAISS index
dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(document_embeddings)


print("Embedding dimension:", dimension)
print("FAISS vector count:", index.ntotal)


def retrieve(query, top_k=5):

    query_embedding = model.encode([query])

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

    for score, idx in zip(scores[0], indices[0]):

        result = documents[idx].copy()

        result["score"] = float(score)

        results.append(result)

    return results


query = "Bu standardın amacı nedir?"

results = retrieve(query, top_k=5)


print("\nQUESTION:")
print(query)

print("\nRETRIEVAL RESULTS:")

for result in results:

    print("\n" + "-" * 60)

    print(f"Score: {result['score']:.4f}")
    print(f"Document: {result['document']}")
    print(f"Page: {result['page']}")
    print(f"Chunk: {result['chunk_id']}")
    print("Text:")
    print(result["text"][:500])