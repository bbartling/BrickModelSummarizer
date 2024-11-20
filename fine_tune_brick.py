import os
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TrainerCallback
from functools import partial
import matplotlib.pyplot as plt


# Define the directories and additional JSON file paths
brick_json_directory = r'C:\Users\bbartling\Desktop\my-own-llm\brick_training_data\processed_fine_tune_data'

additional_json_data = [
    r'C:\Users\bbartling\Desktop\data\instruction-examples.json',
    r'C:\Users\bbartling\Desktop\data\brick-concepts.json',
    r'C:\Users\bbartling\Desktop\data\hvac-controls.json',
    r'C:\Users\bbartling\Desktop\data\iaq-concepts.json',
]

# Initialize a list to hold all training data
train_data = []

# Process the JSON files in the directory
for filename in os.listdir(brick_json_directory):
    if filename.endswith('.json'):  # Only process JSON files
        file_path = os.path.join(brick_json_directory, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):  # If the file contains a list of entries
                    train_data.extend(data)
                else:  # If the file contains a single entry
                    train_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {filename}: {e}")

# Process each additional JSON file in the list
for additional_file in additional_json_data:
    try:
        with open(additional_file, 'r', encoding='utf-8') as f:
            additional_data = json.load(f)
            if isinstance(additional_data, list):  # If the file contains a list of entries
                train_data.extend(additional_data)
            else:  # If the file contains a single entry
                train_data.append(additional_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {additional_file}: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {additional_file}")

# Output the number of entries loaded
print(f"Loaded {len(train_data)} entries from directory and additional JSON files.")

# Save combined dataset to a new JSON file
output_file = r'C:\Users\bbartling\Desktop\my-own-llm\combined_training_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(train_data, f, indent=4, ensure_ascii=False)

print(f"Combined dataset saved to {output_file}.")

# Custom callback to log training losses
class LossLoggerCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if 'loss' in logs:
            loss_values.append(logs['loss'])

# Custom function to format instruction-based entries
def format_input(entry):
    instruction_text = (
        f"Below is an instruction that describes a task. "
        f"Write a response that appropriately completes the request."
        f"\n\n### Instruction:\n{entry['instruction']}"
    )
    input_text = f"\n\n### Input:\n{entry['input']}" if entry["input"] else ""
    return instruction_text + input_text

# Custom Dataset for instruction data
class InstructionDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer
        self.encoded_texts = []
        
        # Pre-tokenize data
        for entry in data:
            instruction_plus_input = format_input(entry)
            response_text = f"\n\n### Response:\n{entry['output']}"
            full_text = instruction_plus_input + response_text
            encoded = tokenizer(full_text, truncation=True, padding='max_length', max_length=512, return_tensors="pt")
            self.encoded_texts.append(encoded)

    def __getitem__(self, index):
        return {
            "input_ids": self.encoded_texts[index]["input_ids"].squeeze(),
            "labels": self.encoded_texts[index]["input_ids"].squeeze(),
        }

    def __len__(self):
        return len(self.data)

# Custom collate function to handle padding
def custom_collate_fn(batch, pad_token_id=50256):
    input_ids = [item["input_ids"] for item in batch]
    labels = [item["labels"] for item in batch]
    
    input_ids = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=pad_token_id)
    labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=pad_token_id)
    
    return {"input_ids": input_ids, "labels": labels}

# Initialize tokenizer and model
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(model_name)

# Prepare dataset and dataloader
train_dataset = InstructionDataset(train_data, tokenizer)
train_loader = DataLoader(
    train_dataset,
    batch_size=8,
    collate_fn=partial(custom_collate_fn, pad_token_id=tokenizer.pad_token_id),
    shuffle=True
)


training_args = TrainingArguments(
    output_dir="./gpt2-fine-tuned-brick",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,  # Accumulate gradients for every 4 steps
    learning_rate=5e-5,
    save_steps=50,
    save_total_limit=2,
    logging_steps=10,
)


# Trainer setup with callback
loss_values = []  # Initialize list for storing losses
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    callbacks=[LossLoggerCallback()]  # Attach the custom callback
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
trainer.save_model('./gpt2-fine-tuned-brick')
tokenizer.save_pretrained('./gpt2-fine-tuned-brick')

# Plotting training loss after training
if loss_values:
    steps = list(range(1, len(loss_values) + 1))
    plt.plot(steps, loss_values, label="Training Loss")
    plt.xlabel("Steps")
    plt.ylabel("Loss")
    plt.title("Training Loss Over Steps")
    plt.legend()
    plt.show()
else:
    print("No loss values were recorded during training.")

print("ALL DONE.")
