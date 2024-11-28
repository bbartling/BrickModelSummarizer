from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
import os

# Path to the text file
TEXT_FILE = "ttl_to_text_description/processed_data/acad.txt"
INDEX_PATH = "building_index"

def prepare_data(file_path):
    """
    Reads the text file and splits it into smaller chunks for indexing.
    """
    chunks = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_chunk = ""
        for line in lines:
            if line.strip():
                current_chunk += line.strip() + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
    return chunks

def index_data(chunks, embedding_model='all-MiniLM-L6-v2', index_path=INDEX_PATH):
    """
    Creates an FAISS index for the text chunks.
    """
    model = SentenceTransformer(embedding_model)
    faiss_index = FAISS.from_texts(chunks, embedding=model)
    faiss_index.save_local(index_path)
    print(f"Index created and saved at {index_path}")
    return faiss_index

def load_index(index_path=INDEX_PATH, embedding_model='all-MiniLM-L6-v2'):
    """
    Loads an existing FAISS index.
    """
    model = SentenceTransformer(embedding_model)
    return FAISS.load_local(index_path, embedding=model)

def query_data(query, index, embedding_model='all-MiniLM-L6-v2', top_k=5):
    """
    Retrieves the most relevant chunks for the given query.
    """
    model = SentenceTransformer(embedding_model)
    query_embedding = model.encode([query])
    docs = index.similarity_search_by_vector(query_embedding, k=top_k)
    return docs

def generate_response(query, index):
    """
    Generates a response based on the retrieved data.
    """
    docs = query_data(query, index)
    response = "Based on your query, the following relevant information was found:\n"
    for i, doc in enumerate(docs, 1):
        response += f"{i}. {doc}\n"
    return response

if __name__ == "__main__":
    # Ensure text file exists
    if not os.path.exists(TEXT_FILE):
        raise FileNotFoundError(f"Text file {TEXT_FILE} not found!")

    # Step 1: Prepare Data
    print("Preparing data...")
    chunks = prepare_data(TEXT_FILE)

    # Step 2: Index Data (only if the index doesn't already exist)
    if not os.path.exists(f"{INDEX_PATH}.faiss"):
        print("Indexing data...")
        index = index_data(chunks)
    else:
        print("Loading existing index...")
        index = load_index()

    # Step 3: Query Example
    print("\nReady for queries!")
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        response = generate_response(query, index)
        print(response)
