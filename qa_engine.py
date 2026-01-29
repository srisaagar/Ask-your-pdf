from embeddings import PDFVectorStore
from ollama_llm import stream_ollama


def split_text(text, chunk_size=500, overlap=100):
    """
    Split PDF text into overlapping chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


def answer_from_pdf_stream(question, chunks, history=""):
    vector_store = PDFVectorStore()
    vector_store.build_index(chunks)

    # Retrieve more chunks for better grounding
    relevant_chunks = vector_store.search(question, top_k=3)

    # Attach chunk references
    context_blocks = []
    for i, chunk in enumerate(relevant_chunks, 1):
        context_blocks.append(f"[SOURCE {i}]\n{chunk}")

    context = "\n\n".join(context_blocks)[:1600]

    prompt = f"""
You are an AI assistant answering questions ONLY from the given PDF content.

{history}

PDF CONTENT WITH SOURCES:
{context}

CURRENT QUESTION:
{question}

INSTRUCTIONS:
- Use ONLY the PDF content
- If numbers are present, you may calculate totals
- Show results clearly
- Structure the answer like this:

SUMMARY:
(short answer)

DETAILS:
(bulleted or step-by-step explanation)

SOURCE:
(Source 1, Source 2, etc.)

If answer not found, say:
"Answer not found in the document."
"""

    return stream_ollama(prompt)

