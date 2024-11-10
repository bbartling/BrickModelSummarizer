from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import torch
import os
import glob
from datasets import Dataset
import matplotlib.pyplot as plt
from transformers import TrainerCallback



# Custom callback to log losses
class LossLoggerCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if 'loss' in logs:
            loss_values.append(logs['loss'])


# Disable GPU if not desired
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


# Load GPT-2 model and tokenizer
model_name = 'gpt2'  # Choose model size as needed ('gpt2', 'gpt2-medium', etc.)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Set padding token for GPT-2
model = GPT2LMHeadModel.from_pretrained(model_name)

# Load conversational training data
train_texts = []
data_dir = "./data/"  # Directory containing training text files

for filepath in glob.glob(data_dir + "*.txt"):
    with open(filepath, "r") as file:
        train_texts.append(file.read().strip())

# Create a dataset from the loaded text
dataset = Dataset.from_dict({"text": train_texts})

# Tokenize the dataset and include labels for text generation
def tokenize_function(examples):
    tokenized_inputs = tokenizer(examples['text'], truncation=True, padding='max_length', max_length=512)
    tokenized_inputs["labels"] = tokenized_inputs["input_ids"].copy()  # Set labels as input_ids for language modeling
    return tokenized_inputs

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Define training arguments with frequent logging
training_args = TrainingArguments(
    output_dir="C:/Users/bbartling/Desktop/my-own-llm/gpt2-fine-tuned",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=50,
    save_total_limit=2,
    logging_steps=1,  # Log every step for detailed tracking
)

# Trainer setup with callback
loss_values = []  # Initialize list for storing losses

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    callbacks=[LossLoggerCallback()],  # Attach the custom callback
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
trainer.save_model('./gpt2-fine-tuned')
tokenizer.save_pretrained('./gpt2-fine-tuned')

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
