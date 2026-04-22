def structure_text(text: str) -> list:

    sections = []
    current_section = {"title": "General", "content": ""}

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue
        
        if line.isupper() or line.endswith(":"):
            if current_section["content"]:
                sections.append(current_section)

            current_section = {
                "title": line,
                "content": ""
            }
        else:
            current_section["content"] += " " + line

    # Add last section
    if current_section["content"]:
        sections.append(current_section)

    return sections