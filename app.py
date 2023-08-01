import streamlit as st
from dotenv import load_dotenv
import time
from llama_cpp import Llama
import pickle
import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import glob
import os
import pickle
import argparse

# ran on Windows 10
# py -3.10 -m streamlit run app.py -- --show_prompt_template

parser = argparse.ArgumentParser()
parser.add_argument(
    "--show_prompt_template",
    action="store_true",
    help="Show the prompt engineering template and response from information retrieval preprocessing",
)
args = parser.parse_args()
print("args.show_prompt_template: \n",args.show_prompt_template)

# Directory path where the .pkl files are located
pkl_directory = "my_data"

# Get a list of all .pkl files in the directory
pkl_files = glob.glob(os.path.join(pkl_directory, "*.pkl"))

# Ensure that there is exactly one .pkl file in the directory
if len(pkl_files) != 1:
    raise ValueError("There should be exactly one .pkl file in the directory")

# Load data from the .pkl file
pkl_file_path = pkl_files[0]
print(pkl_file_path)
with open(pkl_file_path, "rb") as file:
    VECTOR_STORES = pkl_file_path


llm = Llama(model_path="./model/ggml-vicuna-7b-1.1-q4_1.bin", n_ctx=3000, n_batch=128)


# Sidebar contents
with st.sidebar:
    st.title("An LLM 💬 App")
    st.markdown(
        """
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [LlamaCpp Embeddings](https://python.langchain.com/docs/integrations/llms/llamacpp)
    - [LlamaCpp Python](https://llama-cpp-python.readthedocs.io/en/latest/)
 
    """
    )


load_dotenv()


def prompt_template(question, insights_data):
    # Create a template for prompting
    template = f"""Question: {question}\n\nAnswer: Let's work this out in a step-by-step way to be sure we have the right answer.
    \n\n The user may be trying to ask about this area of interest {insights_data}
    """
    return template


# Set up the CallbackManager for token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


def generate_text(
    prompt, max_tokens=3000, temperature=0.1, top_p=0.5, echo=False, stop=[]
):
    start_time = time.time()
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stop=stop,
    )
    end_time = time.time()
    time_taken = end_time - start_time
    output_text = output["choices"][0]["text"].strip()
    return output_text, time_taken


def main():
    st.title("LlamaCpp Python LLM")
    st.write("With a RAG inspired information retrieval preprocessing")

    if os.path.exists(VECTOR_STORES):
        with open(VECTOR_STORES, "rb") as f:
            VectorStore = pickle.load(f)
        st.success(f"Using store name: {VECTOR_STORES}")

    prompt = st.text_input("Enter a question in prompt:")

    if st.button("Generate Response from the LMM"):
            
        vector_data = VectorStore.similarity_search(query=prompt, k=3)

        # Print the vector_data for debugging or observation
        #print("vector_data: \n", vector_data)

        insights = ""
        # Loop through the vector_data list and extract the page content for each document
        for info in vector_data:
            info_content = info.page_content
            print("---------------")
            print(info_content)
            print("---------------")
            insights += info_content + " " 
            
        prompt_finalized = prompt_template(prompt, insights)
        if args.show_prompt_template:
            st.warning(f"prompt_finalized \n {prompt_finalized}")
        st.info("Generating responce from the LLM...this may take a little bit")
                
        result, inference_time = generate_text(
            prompt_finalized, max_tokens=3000
        )
        
        minutes, seconds = divmod(inference_time, 60)
        st.write(f"Model inference time: {int(minutes)}m {int(seconds)}s")
        st.success(result)


if __name__ == "__main__":
    main()

