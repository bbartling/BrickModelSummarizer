from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(text, chunk_size, overlap):
    """
    Split the text into chunks of the specified size with an overlap.
    
    Parameters:
    - text (str): The input text to be split.
    - chunk_size (int): The size of each chunk.
    - overlap (int): The size of the overlap between chunks.
    
    Returns:
    - list of str: The split text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# Define an HVAC-related query
query = ['How does a central air conditioning system work?']

# Load the text file from the data subdirectory
with open('data/hvac.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split the content using the text splitter utility
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Use the function to split the content
sections = split_text_into_chunks(content, 1000, 200)

# Assuming the provided model name remains the same
model = SentenceTransformer('paraphrase-distilroberta-base-v2')

# Generate embeddings
query_embeddings = model.encode(query)
sections_embeddings = model.encode(sections)

# Compute similarity
similarities = cosine_similarity(query_embeddings, sections_embeddings)

# Get the index of the most similar document
retrieved_doc_id = np.argmax(similarities[0])

print("Most relevant chunk to the query:\n")
print(sections[retrieved_doc_id])
