
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load models once
sentence_transformer_model = SentenceTransformer('paraphrase-distilroberta-base-v2')
llm = Llama(model_path="ggml-vicuna-7b-1.1-q4_1.bin", n_ctx=512, n_batch=126)

def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def retrieve_most_relevant_chunk(query, sections):
    """
    Retrieve the most relevant chunk from sections based on a query.
    """
    query_embeddings = sentence_transformer_model.encode([query])
    sections_embeddings = sentence_transformer_model.encode(sections)
    similarities = cosine_similarity(query_embeddings, sections_embeddings)
    retrieved_doc_id = np.argmax(similarities[0])
    return sections[retrieved_doc_id]

def generate_text(prompt, max_tokens=256, temperature=0.1, top_p=0.5, echo=False, stop=["#"]):
    """
    Generate text using the Llama model.
    """
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stop=stop,
    )
    return output["choices"][0]["text"].strip()

def main():
    with open('data/hvac.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    while True:
        prompt = input("\nEnter a prompt (or type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        else:
            print("\nFinding the most relevant section...")
            relevant_section = retrieve_most_relevant_chunk(prompt, split_text_into_chunks(content))
            
            print("\nGenerating text...\n")
            result = generate_text(relevant_section, max_tokens=356)
            print(result)

if __name__ == "__main__":
    main()
