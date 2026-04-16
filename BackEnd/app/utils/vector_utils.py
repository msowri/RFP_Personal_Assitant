def to_pgvector(vec: list[float]) -> str:
    """Convert Python list → pgvector string"""
    return "[" + ",".join(map(str, vec)) + "]"