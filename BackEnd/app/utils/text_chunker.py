
def chunk_text(text: str, chunk_size=500, overlap=50): # overlap added to and from continue
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks