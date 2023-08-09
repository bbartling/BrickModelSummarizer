import streamlit as st
from ctransformers import AutoModelForCausalLM
from dotenv import load_dotenv
import pickle
import argparse

# ran on Windows 10
# py -3.10 -m streamlit run app.py -- --use_word_embeddings

MODEL = "./model/llama-2-7b-chat.ggmlv3.q2_K.bin"
# MODEL = "./model/llama-2-7b-chat.ggmlv3.q6_K.bin"

EMBEDDINGS = "./my_data/hvac_llama-2-7b-chat.ggmlv3.q2_K.pkl"
# EMBEDDINGS = "./my_data/hvac_llama-2-7b-chat.ggmlv3.q6_K.pkl"

CHUNKS = 3

parser = argparse.ArgumentParser()
parser.add_argument(
    "--use_word_embeddings",
    action="store_true",
    help="Use word embeddings in vector stores (.pkl file) to incorporate your own data into the question to the LLM",
)
args = parser.parse_args()
print("args.user_vector_stores: \n", args.use_word_embeddings)

# Load data from the .pkl file
with open(EMBEDDINGS, "rb") as f:
    VectorStore = pickle.load(f)


# Sidebar contents
with st.sidebar:
    st.title("An LLM 💬 App")
    st.markdown(
        """
    ## About
    This app is an LLM-powered chatbot built using:
    - [Llama Cpp](https://github.com/ggerganov/llama.cpp)
    - [LlamaCpp Embeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.llamacpp.LlamaCppEmbeddings.html)
    - [ctransformers](https://github.com/marella/ctransformers)
     - [LangChain](https://python.langchain.com/)
    """
    )

load_dotenv()


@st.cache_resource()
def ChatModel(temperature, top_p):
    return AutoModelForCausalLM.from_pretrained(
        MODEL, model_type="llama", temperature=temperature, top_p=top_p
    )


# Replicate Credentials
with st.sidebar:
    st.subheader("Models and parameters")

    temperature = st.sidebar.slider(
        "temperature", min_value=0.01, max_value=2.0, value=0.1, step=0.01
    )
    top_p = st.sidebar.slider(
        "top_p", min_value=0.01, max_value=1.0, value=0.9, step=0.01
    )
    token_input = st.sidebar.slider(
        "tokens", min_value=64, max_value=4096, value=512, step=8
    )
    chat_model = ChatModel(temperature, top_p)


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


st.sidebar.button("Clear Chat History", on_click=clear_chat_history)


# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = """You are a helpful assistant. You do not respond as 
    'User' or pretend to be 'User'. You only respond once as 'Assistant'."""

    if args.use_word_embeddings:
        vector_stores = generate_vector_stores(prompt_input)
        vector_stores_final = (
            string_dialogue
            + f" The user may need help in this area of expertise {vector_stores}"
        )
        print("vector_stores_final: \n", vector_stores_final)

    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
    output = chat_model(f"prompt {string_dialogue} {prompt_input} Assistant: ")
    return output


def generate_vector_stores(question):
    vector_data = VectorStore.similarity_search(query=question, k=CHUNKS)

    insights = ""
    # Loop through the vector_data list and extract the page content for each document
    for info in vector_data:
        info_content = info.page_content
        insights += info_content + " "

    return insights


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ""
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
