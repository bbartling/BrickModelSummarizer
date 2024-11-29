import os
import pickle

# Path to the existing pickle file
PICKLE_PATH = "acad.pkl"
BRICK_IN_TEXT_FILE_PATH = r"C:\Users\bbartling\Desktop\my-own-llm\ttl_to_text_tests\processed_data\acad.txt"

print("Loading Text File: \n", BRICK_IN_TEXT_FILE_PATH)

def load_index(pickle_path):
    """
    Load the FAISS index from the pickle file.
    """
    if not os.path.exists(pickle_path):
        raise FileNotFoundError(f"Pickle file {pickle_path} not found! Please create the index first.")
    with open(pickle_path, "rb") as f:
        index = pickle.load(f)
    print(f"Index loaded from {pickle_path}")
    return index

def query_index(index, query, top_k=2):
    """
    Perform a query on the loaded FAISS index.
    """
    results = index.similarity_search(query, k=top_k)
    return results

if __name__ == "__main__":
    # Step 1: Load Existing Index
    print("Loading existing index...")
    index = load_index(PICKLE_PATH)

    # Step 2: Query the Index
    print("\nReady for queries!")
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = query_index(index, query)
        print("\nRelevant Information:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.page_content}")
