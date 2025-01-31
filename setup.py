from setuptools import setup, find_packages


def read_long_description(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()


setup(
    name="brick_model_summarizer",
    version="0.4.1",
    author="Ben Bartling",
    author_email="ben.bartling@gmail.com",
    description="A package for summarizing BRICK models",
    long_description=read_long_description("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/bbartling/BrickModelSummarizer",
    packages=find_packages(
        include=["brick_model_summarizer", "brick_model_summarizer.*"]
    ),
    install_requires=[
        "black",
        "rdflib",
        "pytest",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
