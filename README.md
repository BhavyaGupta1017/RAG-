# 📚 Chat with Your PDF — RAG Project

A Retrieval-Augmented Generation (RAG) application that lets users upload a PDF, search its contents using semantic embeddings, and ask questions answered by Google Gemini using retrieved passages.

## Features

- Upload a PDF through a Streamlit interface
- Extract selectable text page by page using PyPDF
- Split text into overlapping chunks
- Create sentence embeddings with HuggingFace Sentence Transformers
- Store and retrieve vectors with FAISS
- Generate grounded answers using Gemini
- Display source passages and PDF page numbers
- Avoid making up answers when the retrieved context does not contain the information

## Project structure

```text
PDF_RAG_Chatbot/
├── .streamlit/
│   └── config.toml
├── app.py
├── main.py
├── requirements.txt
├── packages.txt
├── .gitignore
├── README.md
└── pdf_ocr_cache.json
```

## Run locally

### 1. Install Python

Use Python 3.10 or newer.

### 2. Open the project folder in a terminal

```bash
cd PDF_RAG_Chatbot
```

### 3. Create and activate a virtual environment (recommended)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the app

```bash
streamlit run app.py
```

Open the local URL printed in the terminal (usually http://localhost:8501).

## Gemini API key

Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

You can paste the key into the app's sidebar while testing locally. For deployment, create a Streamlit secret named `GEMINI_API_KEY`:

```toml
GEMINI_API_KEY = "paste-your-key-here"
```

Do not commit API keys or `.streamlit/secrets.toml` to GitHub.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/).
3. Choose **Create app** and select your repository.
4. Set the main file path to `app.py`.
5. In app settings, add `GEMINI_API_KEY` under Secrets.
6. Deploy.

The first deployment may take a few minutes because the embedding model is downloaded.

## Notes and limitations

- This starter version processes one uploaded PDF at a time.
- The PDF needs selectable text. Scanned/image-only PDFs require OCR first.
- The FAISS index is held in session memory and is rebuilt when a PDF is processed.
- Do not upload confidential documents to a public demo.
- Gemini API usage may be subject to quotas and billing terms.
