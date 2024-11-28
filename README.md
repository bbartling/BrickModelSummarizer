# HvacGPT

**⚠️👷🚧🏗️ WARNING** - This project is new and highly experimental! Its in the process of getting mega overhauls but the idea is to make an LLM assistant for the building operator.

1. **Tested on Windows Python 3.12**  
   Download Python
   * https://www.python.org/downloads/windows/

2. **Create a Virtual Environment**  
   In Windows PowerShell set up a virtual environment to manage dependencies.

   ```sh
   py -m venv env
   ```

3. **Activate the Environment**  
   On Windows, activate the virtual environment:

   ```sh
   env\Scripts\activate
   ```

4. **Install Dependencies**  
   Install the necessary Python packages with pip.

   ```sh
   pip install --upgrade pip sentence-transformers langchain faiss-cpu rdflib tf-keras tensorflow pandas matplotlib
   ```


## Licence

【MIT License】

Copyright 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
