import torch
import torch.nn as nn
from encoder import TransformerEncoderLayer
from decoder import TransformerDecoderLayer

class Transformer(nn.Module):
    def __init__(self, num_layers, d_model, num_heads, dff, dropout_rate=0.1):
        super(Transformer, self).__init__()
        self.encoder_layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, dff, dropout_rate) for _ in range(num_layers)
        ])
        self.decoder_layers = nn.ModuleList([
            TransformerDecoderLayer(d_model, num_heads, dff, dropout_rate) for _ in range(num_layers)
        ])
        self.final_layer = nn.Linear(d_model, 1)

    def forward(self, input_ids, target_ids, attention_mask=None):
        enc_output = input_ids
        for encoder in self.encoder_layers:
            enc_output = encoder(enc_output, attention_mask)

        dec_output = target_ids
        for decoder in self.decoder_layers:
            dec_output = decoder(dec_output, enc_output, attention_mask)

        return torch.sigmoid(self.final_layer(dec_output[:, 0, :]))  # Binary output
