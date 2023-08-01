
This is an attempt at something similar to RAG.

**SentenceTransformer Embeddings**: It utilizes the paraphrase-distilroberta-base-v2 model from the sentence_transformers library to generate semantic embeddings. This process enhances similarity comparisons between different pieces of content.

**Cosine Similarity**: The project employs cosine similarity metrics from sklearn to measure semantic closeness between the user's query and pre-defined content chunks.

**Text Splitter**: To achieve more accurate retrievals, a custom-defined function is used to split large text into manageable chunks with an overlap.

Additionally, within the `my_data` subdirectory, two Python scripts are provided to convert PDF or Word documents into text files. These scripts will loop over the directory to find files with these extensions and merge their contents into one text file. The text file needs to be cleaned before the LLM script can use it with the RAG-inspired data retrieval approach and the prompt engineering template.

To execute the script, run the following command in the terminal:
``` bash
$ python similarities_testing.py
```

