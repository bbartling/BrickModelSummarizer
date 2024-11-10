from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load the original GPT-2 model and tokenizer
original_model_name = "gpt2"
original_tokenizer = GPT2Tokenizer.from_pretrained(original_model_name)
original_model = GPT2LMHeadModel.from_pretrained(original_model_name)
original_tokenizer.pad_token = original_tokenizer.eos_token  # Set padding token for consistency

# Load the fine-tuned GPT-2 model and tokenizer
fine_tuned_dir = "./gpt2-fine-tuned"  # Directory where fine-tuned model is saved
fine_tuned_tokenizer = GPT2Tokenizer.from_pretrained(fine_tuned_dir)
fine_tuned_model = GPT2LMHeadModel.from_pretrained(fine_tuned_dir)
fine_tuned_tokenizer.pad_token = fine_tuned_tokenizer.eos_token

# Set models to evaluation mode
original_model.eval()
fine_tuned_model.eval()

# Function to generate a response from a model
def generate_response(model, tokenizer, prompt, max_length=100):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Main interaction loop
def main():
    print("Type 'exit' to quit the program.")
    while True:
        prompt = input("Enter a prompt: ")
        if prompt.lower() == 'exit':
            break

        print("\n--- Original GPT-2 Response ---")
        original_response = generate_response(original_model, original_tokenizer, prompt)
        print(original_response)

        print("\n--- Fine-Tuned GPT-2 Response ---")
        fine_tuned_response = generate_response(fine_tuned_model, fine_tuned_tokenizer, prompt)
        print(fine_tuned_response)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
