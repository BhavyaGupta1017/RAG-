# 📚 PDF RAG Chatbot

An AI-powered PDF Question Answering Chatbot built using **Streamlit, Google Gemini API, FAISS, and Sentence Transformers**. Upload a PDF document and ask questions about its content in natural language.

The chatbot retrieves relevant passages from the uploaded PDF and uses Gemini to generate concise, context-based answers with page references.

## ✨ Features

- 📄 **PDF Text Extraction** — Extracts text from PDF documents using PyPDF.
- ✂️ **Text Chunking** — Splits extracted text into smaller, overlapping chunks.
- 🧠 **Semantic Embeddings** — Converts text into vector representations using Sentence Transformers.
- 🔎 **FAISS Vector Search** — Retrieves relevant passages based on the user's question.
- 🤖 **AI-Powered Answers** — Uses the Google Gemini API to answer questions from retrieved PDF passages.
- 📌 **Page References** — Includes relevant PDF page numbers in answers.
- 🔄 **Error Handling** — Retries temporary Gemini API errors and supports model fallback.
- 🌙 **Dark UI** — Provides a clean, dark-themed chat interface using Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Google Gemini API | AI-generated answers |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| PyPDF | PDF text extraction |
| NumPy | Numerical and vector operations |

## 📂 Project Structure

```text
PDF_RAG_Chatbot/
│
└── Chatbot/
    ├── app.py
    ├── main.py
    ├── requirements.txt
    ├── packages.txt
    ├── README.md
    ├── pdf_ocr_cache.json
    └── .streamlit/
        └── config.toml
```

*Note: Some files may differ depending on your local setup. Do not upload virtual environments, API keys, or other sensitive files to GitHub.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PDF_RAG_Chatbot/Chatbot
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PyTorch or torchvision installation fails, install compatible versions for your Python environment.

### 4. Get a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Create or obtain a Gemini API key.
3. Run the application and enter the key in the app's Settings section.

**Security:** Never commit your API key to GitHub or include it in screenshots, source code, or public configuration files.

### 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the chatbot.

## 🚀 How It Works

The application follows a Retrieval-Augmented Generation (RAG) pipeline:

1. **Upload PDF:** The user uploads a PDF document.
2. **Text Extraction:** Text is extracted page by page.
3. **Chunking:** The extracted text is divided into overlapping chunks.
4. **Embedding Generation:** Sentence Transformers converts chunks into embeddings.
5. **Vector Indexing:** FAISS stores the embeddings for similarity search.
6. **Question Retrieval:** The user's question is embedded and matched against relevant PDF chunks.
7. **Answer Generation:** Gemini receives the retrieved passages and the question.
8. **Response Display:** The generated answer and relevant source information are returned to the user.

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Sentence Embeddings
    ↓
FAISS Vector Index
    ↓
Question Embedding
    ↓
Relevant Passage Retrieval
    ↓
Google Gemini API
    ↓
Answer with Page References
```

## 💬 Example Usage

**Example question:**

"What are the five main points discussed in this PDF?"

**Expected workflow:**

- Upload a PDF document.
- Enter your question in the chat interface.
- The application retrieves relevant passages.
- Gemini generates an answer based on those passages.
- Review the answer and cited page numbers against the original PDF.

## ⚠️ Limitations

- Scanned or image-only PDFs may require OCR before their text can be searched.
- Answers depend on the quality of extracted text and retrieved passages.
- Incorrect or incomplete retrieval can affect answer accuracy.
- Gemini API availability, rate limits, and usage quotas may affect response generation.
- API keys must be kept secure.

Always verify important answers against the original document.

## 🔮 Future Improvements

- Support multiple PDF documents in one session.
- Add OCR for scanned PDFs.
- Store vector indexes for faster repeated queries.
- Add chat history and conversation memory.
- Improve source citations and passage highlighting.
- Add support for additional language models.
- Improve error handling, logging, and deployment configuration.

## 🔐 Privacy and Security

PDF content may be sent to the configured AI provider as part of answer generation. Avoid uploading confidential documents unless you are authorized to process them using the selected services.

Never publish API keys, credentials, or private documents in a public repository.

## 👨‍💻 Author

**Your Name**

GitHub: [Your GitHub Profile](https://github.com/)

## 📄 License

This project is available under the MIT License if you choose to distribute it under that license. Add a `LICENSE` file containing the MIT License before claiming that the project is MIT-licensed.
