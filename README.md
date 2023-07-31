# my-own-llm
Concept Idea to run a local LLM locally on CPU trained with assistance with your own data on using something similar to RAG but more simple that can maybe run on resource constraint devices. The project incorporates the [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) project with the the CPU optimized (GGML) models. 

## Data
There is a `my_data` sub directory with a .txt file of application specific data that used in the RAG inspired approch to assist the LLM with a prompt engineering template with these features:
* SentenceTransformer Embeddings: Utilizes the paraphrase-distilroberta-base-v2 model from the sentence_transformers library to generate semantic embeddings for better similarity comparisons.

* Cosine Similarity: Employs cosine similarity metrics from sklearn to measure semantic closeness between the user's query and pre-defined content chunks.

* Text Splitter: Uses a custom-defined function to split large text into manageable chunks with an overlap for more accurate retrievals.

There are two python scripts inside the `my_data` sub directory used to convert PDF or Word docs to text files. Those files will loop over this directory for those file extensions and boil everything down to one text file. The text file needs to be cleaned where then the LLM script will look in this directory a text file to use with the RAG inspired data retreival appraoch and with  the prompt engineering template. Run file like this:

``` bash
$ similarities_testing.py
```

And an Input function in the script will pop up console for you to type commands in to seeing the best data retrieved results from you dataset contained in the .txt file from the `my_data` directory.

## Model
There is a `model` subdirectory with a `download_model.py` when ran will download the `ggml-vicuna-7b-1.1-q4_1.bin` from HuggingFace which is a 4 gig file.

## Testing
And an Input function in the script will pop up console for you to type commands to the LLM. To run LLM locally without any RAG inspired assistance:
``` bash
$ llm_no_sims.py
```
Run LLM locally with RAG inspired assistance:
``` bash
$ llm_with_sims.py
```
TODO: More testing, enhance prompt engineering template, and move prompt engineering template to its own .py file. Do more research about data retrieval results between similarities Vs RAG approach on small datasets.

## Author

[linkedin](https://www.linkedin.com/in/ben-bartling-510a0961/)

## Licence

【MIT License】

Copyright 2022 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
