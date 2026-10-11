# 📄 Document Explainer — Local RAG Application

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents, ask questions in natural language, and receive answers grounded in the document's content.

The application uses locally running AI models to generate embeddings, retrieve relevant passages, and generate answers without requiring a hosted LLM API.

## ✨ Features

- **PDF ingestion:** Extract text from PDF documents using PyMuPDF.
- **Text chunking:** Split extracted text into overlapping chunks for better retrieval.
- **Local embeddings:** Generate text embeddings using Sentence Transformers.
- **Vector search:** Store and retrieve document chunks using ChromaDB.
- **Local LLM:** Generate document-grounded answers using Ollama.
- **Source references:** Display source filenames and page references.
- **Interactive UI:** Upload PDFs and ask questions through Streamlit.
- **Local-first architecture:** Process documents and generate answers locally.

## 🏗️ Architecture

```text
                ┌──────────────────────┐
                │   Streamlit UI       │
                │  Upload PDF / Query  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   PDF Text Extractor │
                │       PyMuPDF        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     Text Chunker     │
                │  Chunking + Overlap  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Sentence Transformers│
                │   Local Embeddings   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │      ChromaDB        │
                │   Vector Retrieval   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │       Ollama         │
                │   Local LLM Answer   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Answer + References  │
                └──────────────────────┘
```

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Package management | uv |
| PDF extraction | PyMuPDF |
| Embeddings | Sentence Transformers |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector database | ChromaDB |
| Local LLM runtime | Ollama |
| Default generation model | `llama3.2:3b` |
| User interface | Streamlit |

## 📋 Prerequisites

Install the following before running the application.

### 1. Python

Python 3.12 or a compatible version satisfying the project requirement.

Verify the installation:

```bash
python --version
```

### 2. uv

Install `uv` by following the instructions at:

https://docs.astral.sh/uv/

Verify the installation:

```bash
uv --version
```

### 3. Ollama

Install Ollama from:

https://ollama.com/download

Download the default language model:

```bash
ollama pull llama3.2:3b
```

Verify that the model is available:

```bash
ollama list
```

Ollama must be running when you ask questions. On systems where Ollama doesn't start automatically, launch it in a separate terminal:

```bash
ollama serve
```

If the Ollama service is already running, do not start a second instance.

### 4. Git

Git is recommended for cloning the repository and managing changes.

https://git-scm.com/downloads

## 🚀 Installation and Setup

### Step 1: Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd document-extractor
```

Replace `<YOUR_REPOSITORY_URL>` with your Git repository URL.

Alternatively, download the repository and open a terminal in the project directory.

### Step 2: Install Python dependencies

```bash
uv sync
```

This creates or updates the project environment using `pyproject.toml` and `uv.lock`.

If dependencies have not yet been added to the project, install them using:

```bash
uv add pymupdf sentence-transformers chromadb ollama streamlit
```

### Step 3: Download the embedding model

The Sentence Transformers model is downloaded automatically the first time it is initialized.

The default embedding model is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

An internet connection may be required for the initial download. Subsequent runs can use the cached model files.

### Step 4: ▶️ Run the Application

From the project root, start Streamlit:

```bash
uv run streamlit run src/document_extractor/streamlit_app.py
```

Open the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

### Using the application

1. Upload a PDF document.
2. Click **Process PDF** to extract, chunk, embed, and index its contents.
3. Enter a question about the document.
4. Click **Get answer**.
5. Review the generated answer and expand **Retrieved passages** to inspect the supporting evidence.


The application should return an answer based on the retrieved document passages, together with source references.

## 🧪 Run the Command-Line Pipeline

The ingestion and retrieval pipeline can also be run without the Streamlit UI:

```bash
uv run python -m document_extractor.test_pipeline
```

Enter the PDF path when prompted, for example:

```text
docs/sample.pdf
```

Then ask a question about the document.

## 📁 Project Structure

```text
document-extractor/
├── src/
│   └── document_extractor/
│       ├── __init__.py
│       ├── pdf_loader.py
│       ├── chunker.py
│       ├── embedder.py
│       ├── vector_store.py
│       ├── answer_generator.py
│       ├── test_pipeline.py
│       └── streamlit_app.py
├── tests/
├── docs/
├── data/
│   └── chroma_db/
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

The `data/chroma_db/` directory is generated locally and contains the persistent vector database. It should not be committed to the public repository.


## 👨‍💻 Author : Vishwajit Dandage

Developed as a hands-on project exploring local LLMs, Retrieval-Augmented Generation, Python, and AI application engineering.