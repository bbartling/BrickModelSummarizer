import streamlit as st
from dotenv import load_dotenv
import time
from llama_cpp import Llama
import pickle
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pickle
import argparse
from prompt_eng_template import prompt_template

# ran on Windows 10
# py -3.10 -m streamlit run app.py -- --show_prompt_template

MODEL = "./model/llama-2-7b-chat.ggmlv3.q2_K.bin"
#MODEL = "./model/llama-2-7b-chat.ggmlv3.q6_K.bin"

EMBEDDINGS = "./my_data/hvac_llama-2-7b-chat.ggmlv3.q2_K.pkl"
#EMBEDDINGS = "./my_data/hvac_llama-2-7b-chat.ggmlv3.q6_K.pkl"

llm = Llama(model_path=MODEL, n_ctx=3000, n_batch=128)
print(llm)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--show_prompt_template",
    action="store_true",
    help="Show the prompt engineering template and response from information retrieval preprocessing",
)
args = parser.parse_args()
print("args.show_prompt_template: \n",args.show_prompt_template)

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
    st.title("My Own Llm With Llama Cpp Python!")

    # Load data from the .pkl file
    with open(EMBEDDINGS, "rb") as f:
        VectorStore = pickle.load(f)

    prompt = st.text_input("Enter a question in prompt:")

    if st.button("Generate Response from the LMM"):
            
        vector_data = VectorStore.similarity_search(query=prompt, k=3)

        insights = ""
        # Loop through the vector_data list and extract the page content for each document
        for info in vector_data:
            info_content = info.page_content
            insights += info_content + " " 
            
        print("insights: \n",insights)
        prompt_finalized = prompt_template(prompt, insights)
        
        if args.show_prompt_template:
            st.write(f"prompt template: \n {prompt_finalized}")
        st.info("Generating responce from the LLM...this may take a little bit")
        
        result, inference_time = generate_text(
            prompt_finalized, max_tokens=3000
        )
        
        minutes, seconds = divmod(inference_time, 60)
        st.write(f"Model inference time: {int(minutes)}m {int(seconds)}s")
        st.success(result)


if __name__ == "__main__":
    main()

