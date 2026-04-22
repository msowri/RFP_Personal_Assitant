def chunk_sections(sections, chunk_size=500, overlap=50):
    chunks = []

    for section in sections:
        text = section["content"]

        start = 0
        while start < len(text):
            chunk_text = text[start:start + chunk_size]

            chunks.append({
                "title": section["title"],
                "text": chunk_text
            })

            start += chunk_size - overlap

    return chunks