import pymupdf


pdf_path = "manual.pdf"


def chunk_text(text, chunk_size=120, overlap=30):

    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        if chunk:
            chunks.append(chunk)

    return chunks


pdf = pymupdf.open(pdf_path)

documents = []

chunk_counter = 1


for page_number, page in enumerate(pdf, start=1):

    text = page.get_text()

    chunks = chunk_text(
        text,
        chunk_size=120,
        overlap=30
    )

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


print("Page count:", len(pdf))
print("Total chunks:", len(documents))


for document in documents[:5]:

    print("\n" + "-" * 50)
    print("Document:", document["document"])
    print("Page:", document["page"])
    print("Chunk:", document["chunk_id"])
    print("Text:")
    print(document["text"][:500])