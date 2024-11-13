# HvacGPT

This is a hobby project aimed at experimenting with fine-tuning the GPT-2 language model using instruction-based data. The goal is to learn how to customize a pre-trained language model to generate responses tailored to specific types of questions or instructions by fine-tuning it on a set of curated examples. Ultimately, this project explores whether an LLM can be specifically tuned for the HVAC industry, enabling it to "think" like an HVAC engineer right out of the box, even without additional context. Ideally, such a model could assist with tasks like fault detection, Automated Supervisory Optimization (ASO) strategies for building efficiency, and interact with structured building data using the BRICK schema.

## What is GPT-2?

GPT-2 is a large language model developed by OpenAI, designed to generate human-like text based on input prompts. It's pre-trained on a massive amount of internet data, which makes it versatile but general in its knowledge and style. By fine-tuning GPT-2, you can specialize it to perform more specific tasks, such as answering technical questions, generating creative writing, or, in this case, responding accurately to instruction-based prompts in the HVAC industry.

## How Fine-Tuning Works

Fine-tuning involves training a pre-trained model (like GPT-2) on a smaller, custom dataset, allowing it to specialize in specific tasks. For this project, we are using a dataset of instruction-following examples, where each example includes an instruction, optional input, and a target response. Fine-tuning GPT-2 on this dataset allows the model to improve its responses to similar instructions, adapting it to follow directions more effectively within the given context.

### Prerequisites
Tested on Windows with Python 3.12. You can download [Python here](https://www.python.org/downloads/).

### Setting Up the Environment

1. **Clone the Repository**  
   Clone this repository to your local machine (or download it as a ZIP file and extract it).


2. **Create a Virtual Environment**  
   Set up a virtual environment to manage dependencies.

   ```sh
   python -m venv env
   ```

3. **Activate the Environment**  
   On Windows, activate the virtual environment:

   ```sh
   env\Scripts\activate
   ```

4. **Install Dependencies**  
   Install the necessary Python packages. Since we’re not using a `requirements.txt` file, you’ll install each package directly:

   ```sh
   pip install torch transformers matplotlib
   ```

### Running the Fine-Tuning Script

Once your environment is set up and dependencies are installed, you can start the fine-tuning process by running the Python script provided in the repository:

```sh
python fine_tune.py
```

This script will load your dataset, tokenize the data, and begin fine-tuning GPT-2 on your custom instructions. Training losses will be logged and plotted after training.

### Files in the Repository

- **`fine_tune.py`** - The main script for loading data, tokenizing, and training the model.
- **`data/`** - Directory containing JSON files with instruction-based examples for fine-tuning.

### Project Goals

The primary goal of this project is to explore how fine-tuning can be used to make GPT-2 more effective at following specific instructions. By the end of the project, you’ll have a better understanding of how to prepare data, set up a training loop, and modify GPT-2 for customized applications.


## Licence

【MIT License】

Copyright 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
