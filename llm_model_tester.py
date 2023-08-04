import time
from llama_cpp import Llama


# ran on windows 10
# $ py -3.10 .\llm_model_tester.py

#llm = Llama(model_path="./model/ggml-vicuna-7b-1.1-q4_1.bin", n_ctx=512, n_batch=126)
llm = Llama(model_path="./model/llama-2-7b-chat.ggmlv3.q6_K.bin", n_ctx=3000, n_batch=512)



def generate_text(
    prompt="",
    max_tokens=3000,
    temperature=0.5,
    top_p=0.5,
    echo=False,
    stop=[],
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


while True:
    prompt = input("\nEnter a prompt (or type 'exit' to quit): ")
    if prompt.lower() == "exit":
        break
    else:
        print("\nGenerating text...\n")
        result, inference_time = generate_text(
            prompt,
            max_tokens=3000
        )
        minutes, seconds = divmod(inference_time, 60)
        print(f"Model inference time: {int(minutes)}m {int(seconds)}s")
        print(result)