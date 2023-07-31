# my-own-llm
My Own Local LLM is a conceptual idea aimed at running a local Language Model (LLM) on a CPU while leveraging your own data, inspired by techniques like [RAG](https://huggingface.co/blog/ray-rag) but designed to be simpler and capable of running on resource-constrained devices.

The project incorporates the [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) project, which brings in compressed CPU-optimized (GGML) models to enhance performance.

The primary goals of this project are to create an easily accessible and efficient solution for running LLMs locally on devices with limited resources, enabling users to utilize their own data for improved performance and flexibility.

Please note that this project is still in its conceptual stage and is actively being developed. Contributions and feedback are welcome as we strive to make this idea a reality.

## Data
The project contains a `my_data` subdirectory that houses a .txt file containing application-specific data, which is used in the RAG-inspired approach to assist the Language Model (LLM) with a prompt engineering template. This template incorporates the following features:

**SentenceTransformer Embeddings**: It utilizes the paraphrase-distilroberta-base-v2 model from the sentence_transformers library to generate semantic embeddings. This process enhances similarity comparisons between different pieces of content.

**Cosine Similarity**: The project employs cosine similarity metrics from sklearn to measure semantic closeness between the user's query and pre-defined content chunks.

**Text Splitter**: To achieve more accurate retrievals, a custom-defined function is used to split large text into manageable chunks with an overlap.

Additionally, within the `my_data` subdirectory, two Python scripts are provided to convert PDF or Word documents into text files. These scripts will loop over the directory to find files with these extensions and merge their contents into one text file. The text file needs to be cleaned before the LLM script can use it with the RAG-inspired data retrieval approach and the prompt engineering template.

To execute the script, run the following command in the terminal:
``` bash
$ python similarities_testing.py
```

Upon running the script, an input function in the script will prompt the user in the console to type commands, leading to the retrieval of the best data results from the dataset contained in the .txt file located within the `my_data` directory. Please note that this project is still under development, and your feedback and contributions are valuable to improve its functionality.

## Model
The `model` subdirectory contains a script named download_model.py. When executed, this script will download the `ggml-vicuna-7b-1.1-q4_1.bin` file from HuggingFace. Please be aware that this model file is relatively large, weighing approximately 4 gigabytes.

The `ggml-vicuna-7b-1.1-q4_1.bin` model is a crucial component of the project, as it provides optimized capabilities for the Language Model (LLM) to operate efficiently.

To obtain the model, run the following command:
``` bash
$ python download_model.py
```
Please ensure that you have sufficient storage space available to accommodate the 4 gigabyte file. Once the download is complete, the model will be ready to be utilized by the LLM for the project's functionalities.

## Testing
To interact with the Language Model (LLM) and evaluate its capabilities, an input function within the script will prompt you to type commands directly into the console.

To run the LLM without any RAG-inspired assistance, execute the following command:
``` bash
$ llm_no_sims.py
```
This command will initiate the LLM, allowing you to explore its functionalities in a standalone mode.

For running the LLM with RAG-inspired assistance, use the following command:
``` bash
$ llm_with_sims.py
```
By executing this command, the LLM will be equipped with the RAG-inspired approach to support its functionalities, making data retrieval more efficient and accurate.

## Next Steps and TODOs

The project is still under development, and there are several tasks to be completed:

1. **Additional Testing**: More extensive testing is needed to ensure the robustness and reliability of the LLM and its various components.

2. **Enhance Prompt Engineering Template**: The prompt engineering template will be further improved to optimize the LLM's performance and response quality.

3. **Modularization**: The prompt engineering template will be moved to its own .py file, promoting better code organization and maintainability.

4. **Research Data Retrieval Results**: Further research is required to compare data retrieval results between the similarity-based approach and the RAG approach, particularly concerning small datasets. This will help identify any trade-offs and strengths of each method.

As development progresses, feedback, contributions, and suggestions from the community will be valuable in refining the project and achieving its goals.


## Author

[linkedin](https://www.linkedin.com/in/ben-bartling-510a0961/)

## Licence

【MIT License】

Copyright 2023 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
