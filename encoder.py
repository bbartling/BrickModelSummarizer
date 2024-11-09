import torch
import torch.nn as nn
from transformers import BertModel


class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, dff, dropout_rate=0.1):
        super(TransformerEncoderLayer, self).__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.fc = nn.Sequential(
            nn.Linear(d_model, dff), nn.ReLU(), nn.Linear(dff, d_model)
        )
        self.layernorm1 = nn.LayerNorm(d_model)
        self.layernorm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        attn_output = outputs.last_hidden_state
        out1 = self.layernorm1(attn_output)
        ffn_output = self.fc(out1)
        out2 = self.layernorm2(out1 + self.dropout(ffn_output))
        return out2
