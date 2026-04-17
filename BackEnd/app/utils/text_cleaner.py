import re
# Removing extra spaces, page numbers, headers, footers, and non-ASCII characters.
# Future enhancements 
def clean_text(text: str) -> str:  
    text = re.sub(r'\s+', ' ', text) # extra space
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE) # page number
    text = re.sub(r'Confidential.*', '', text, flags=re.IGNORECASE) # header and footer
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # weird characters

    return text.strip()