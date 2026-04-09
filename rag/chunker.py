"""
    Chunker:
        spliting abstracts into overlapping chunks
"""

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    words = text.split()#spliting the text by words returning a list
    chunks = []  #a list of strings
    step = chunk_size - overlap #the step we take each time we put a chunk in the chunks list
                                #it ensures the overlap we want which is 20 words
    for i in range(0, len(words), step):
        chunk = words[i:i + chunk_size] #chunk is a list of words from i until i+80 to ensure overlapping
        if len(chunk)<10: #if chunk is less then ten we stop because a chunk that small is meaningles
            break
        chunks.append(" ".join(chunk))#appending a chunk of text after each iteration
    return chunks