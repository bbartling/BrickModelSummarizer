# my-own-llm

This is a Hobby project just for fun to learn how to build a Transformer model with PyTorch and fine-tune a pre-trained language model using Hugging Face Transformers. It includes code for defining Transformer encoder and decoder layers, assembling a full Transformer model, and fine-tuning a BERT model for sentiment analysis.

## BERT

BERT is used as a pre-trained model from Hugging Face’s library, specifically leveraging the `bert-base-uncased` model for various NLP tasks. Let's break down how this is implemented across the files and where the pre-trained BERT model is utilized:

1. **Pre-trained Model Import**: In `decoder.py`, `encoder.py`, and `fine_tune.py`, the BERT model is loaded from Hugging Face's library using:
   ```python
   from transformers import BertModel
   model = BertModel.from_pretrained('bert-base-uncased')
   ```
   This command downloads the pre-trained BERT model (if not already cached) and prepares it for use in your PyTorch models【8†source】【9†source】【11†source】.

2. **Model Usage in Encoder and Decoder**:
   - In `encoder.py`, the `TransformerEncoderLayer` class uses BERT's `last_hidden_state` as part of the transformer’s encoder. This encoded representation is further processed with normalization and a feed-forward layer【10†source】.
   - In `decoder.py`, the `TransformerDecoderLayer` class also uses BERT’s `last_hidden_state` as a base input to decode information. Similar to the encoder, it applies additional transformations and normalization【9†source】.

3. **Fine-Tuning with Transfer Learning**:
   - In `fine_tune.py`, BERT is used as the core of an HVAC chatbot model (`HVACChatbot`). Here, BERT is connected to a custom layer for classifying system statuses as "Good" or "Bad." The fine-tuning process modifies only the additional layers on top of BERT, allowing the model to apply BERT’s language understanding to specific HVAC-related questions and answers【11†source】.

The file `fine_tune.py` provides an example of transfer learning where BERT's pre-trained embeddings are adapted for your specific task (classification of HVAC system statuses). This setup is the “fine-tuning” step, allowing BERT’s general language understanding to be applied to your specific domain.

## More info on BERT
TODO read up on all the links and notebook tutorials on Hugging Face for BERT.
* https://huggingface.co/docs/transformers/en/model_doc/bert

## Licence

【MIT License】

Copyright 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
