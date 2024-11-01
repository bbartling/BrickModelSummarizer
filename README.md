# my-own-llm

This is a Hobby project just for fun to learn how to build a Transformer model with PyTorch and fine-tune a pre-trained language model using Hugging Face Transformers. It includes code for defining Transformer encoder and decoder layers, assembling a full Transformer model, and fine-tuning a BERT model for sentiment analysis.

## File Structure

```plaintext
transformer_project/
├── encoder.py         # Transformer encoder layer
├── decoder.py         # Transformer decoder layer
├── transformer.py     # Full Transformer model
└── fine_tune.py       # Hugging Face fine-tuning script
```

## Requirements

- PyTorch
- Hugging Face Transformers

Install the required libraries:

```bash
pip install torch transformers
```

## Code Overview

1. **`encoder.py`**: Defines the Transformer encoder layer using multi-head attention, feed-forward network, and normalization.
2. **`decoder.py`**: Defines the Transformer decoder layer with self-attention and encoder-decoder attention.
3. **`transformer.py`**: Assembles the Transformer model by combining the encoder and decoder layers.
4. **`fine_tune.py`**: Fine-tunes a pre-trained BERT model from Hugging Face for sentiment analysis.

## Usage

### 1. Define Transformer Components

The files `encoder.py` and `decoder.py` contain classes for the encoder and decoder layers of a Transformer. These files are imported by `transformer.py` and do not need to be run individually.

### 2. Assemble the Transformer Model

The `transformer.py` file creates a full Transformer model by stacking encoder and decoder layers. This file defines the complete model architecture but is not intended to be run directly here.

### 3. Fine-Tune with Hugging Face (`fine_tune.py`)

The main code for loading, fine-tuning, and testing a pre-trained language model is in `fine_tune.py`. This script uses the Hugging Face Transformers library to download and fine-tune a BERT model.

Run the script with:

```bash
python fine_tune.py
```

This script will:
- **Download** the pre-trained `bert-base-uncased` model if it’s not already cached locally.
- **Fine-tune** the BERT model on a sample sentiment analysis task.
- **Test** the model on new sentences to evaluate its performance.
- **TODO** create some training data and something interesting to try in the HVAC/Smart building IoT industry.


## Notes

- GPU is disabled in the `fine_tune.py` with the `os.environ["CUDA_VISIBLE_DEVICES"] = "-1"`.
- You can change the model in `fine_tune.py` by replacing `'bert-base-uncased'` with another model from Hugging Face's Model Hub.
- The downloaded model files will be cached in `~/.cache/huggingface/transformers` by default.


## Licence

【MIT License】

Copyright 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
