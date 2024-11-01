from transformers import BertTokenizer, BertModel
import torch
import torch.nn as nn
import torch.optim as optim
import os
import glob

# Disable GPU if not desired
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Define an HVAC Chatbot model using BERT and a decision layer
class HVACChatbot(nn.Module):
    def __init__(self, bert_model):
        super(HVACChatbot, self).__init__()
        self.bert = bert_model
        self.fc = nn.Linear(bert_model.config.hidden_size, 2)  # 2 outputs for "Good" or "Bad" status
    
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]  # Use the [CLS] token representation
        logits = self.fc(cls_output)
        return torch.softmax(logits, dim=1)  # Softmax for probabilities of "Good" or "Bad"

# Instantiate the model
hvac_model = HVACChatbot(model)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(hvac_model.parameters(), lr=1e-5)

# Load training data from "data" directory
train_sentences = []
train_labels = []
data_dir = "./data/"

for filepath in glob.glob(data_dir + "*.txt"):
    with open(filepath, 'r') as file:
        content = file.read().strip()
        train_sentences.append(content)
        
        # Assign label based on keywords in the filename
        if "good" in filepath.lower():
            train_labels.append(0)  # 0 for "Good"
        elif "bad" in filepath.lower():
            train_labels.append(1)  # 1 for "Bad"

# Convert labels to tensor
train_labels = torch.tensor(train_labels, dtype=torch.long)

# Tokenize input data
inputs = tokenizer(train_sentences, padding=True, truncation=True, return_tensors="pt")

# Training loop
hvac_model.train()
for epoch in range(5):  # More epochs to refine responses
    optimizer.zero_grad()
    outputs = hvac_model(inputs['input_ids'], inputs['attention_mask'])
    loss = criterion(outputs, train_labels)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

# Testing the chatbot with new building operation queries
hvac_model.eval()
test_queries = [
    "The cooling system is not reaching setpoints.",
    "All zones are comfortable and stable.",
    "There's excessive humidity in the lobby.",
    "Heating seems to be working fine in all areas.",
    "Ventilation pressure is too low in zone 4."
]
test_inputs = tokenizer(test_queries, padding=True, truncation=True, return_tensors="pt")

# Predict
with torch.no_grad():
    predictions = hvac_model(test_inputs['input_ids'], test_inputs['attention_mask'])

# Display predictions
for query, prediction in zip(test_queries, predictions):
    status = "Good" if prediction.argmax().item() == 0 else "Bad"
    print(f"Query: '{query}' - System Status: {status}")
