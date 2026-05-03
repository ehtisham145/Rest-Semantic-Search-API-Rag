from langchain_huggingface import HuggingFaceEmbeddings
from pypdf import PdfReader
import io
def extract_text_chunks(pdf_bytes:bytes,chunk_size:int=500)->list[str]:
    """Read a PDF from Raw bytes and split into text chunks"""
    reader=PdfReader(io.BytesIO(pdf_bytes))
    full_text=""
    for page in reader.pages:
        full_text=full_text+page.extract_text() or "" #If a page is empty return empty string
    words=full_text.split()
    chunks=[]
    for i in range(0,len(words),chunk_size):
        chunk=" ".join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

#output of this function will be jsut like that ["Python is a", "very fast and", "easy language learning"]

def get_embeddings(embedding_model,texts: list[str]) -> list[list[float]]:
    """Return a list of embedding vectors for the given texts."""
    return embedding_model.embed_documents(texts)
