# 📚 RAG System with LangChain & Groq

A Retrieval-Augmented Generation (RAG) system that lets you ask questions about any book or document using free AI models.

Built with LangChain, Chroma, HuggingFace Embeddings, and Groq.

---

## 🧠 How it works

1. **Load** — Reads `.md` documents from `data/books/`
2. **Split** — Cuts them into small overlapping chunks
3. **Embed** — Converts chunks into vectors using HuggingFace
4. **Store** — Saves vectors in a local Chroma database
5. **Query** — Searches for relevant chunks and sends them to Groq AI
6. **Answer** — AI answers based only on the retrieved context

---

## 🗂️ Project Structure

rag_langchain_python_project/
├── code/
│   ├── create_database.py   # Builds the vector database
│   └── query_data.py        # Queries the database and gets answers
├── data/
│   └── books/               # Put your .md documents here
├── .env                     # Your secret API keys (never push this!)
├── .env.example             # Template for required keys
├── .gitignore               # Files to exclude from Git
├── requirements.txt         # Python dependencies
└── README.md                # This file

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/rag_langchain_python_project.git
cd rag_langchain_python_project
```

### 2. Create a virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set up your API key
```bash
cp .env.example .env
```
Then open `.env` and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

Get a free key at 👉 https://console.groq.com

---

## 🚀 Usage

### Step 1: Add your documents
Put any `.md` files inside `data/books/`

### Step 2: Build the database
```bash
python code/create_database.py
```

### Step 3: Ask questions
```bash
python code/query_data.py "Your question here"
```

### Example:
```bash
python code/query_data.py "Who is the Queen of Hearts?"
python code/query_data.py "What did the White Rabbit do?"
python code/query_data.py "How did Alice fall into Wonderland?"
```

---

## 🛠️ Functions

### `create_database.py`

| Function | Description |
|---|---|
| `main()` | Entry point, calls generate_data_store |
| `generate_data_store()` | Orchestrates the full pipeline |
| `load_documents()` | Reads all .md files from data/books/ |
| `split_text()` | Splits documents into 300-char chunks with 100-char overlap |
| `save_to_chroma()` | Embeds chunks and saves to Chroma database |

### `query_data.py`

| Function | Description |
|---|---|
| `main()` | Accepts query from terminal, runs full RAG pipeline |

---

## 📦 Tech Stack

| Tool | Purpose |
|---|---|
| LangChain | AI pipeline framework |
| Chroma | Local vector database |
| HuggingFace | Free text embeddings (all-MiniLM-L6-v2) |
| Groq | Free LLM API (llama-3.3-70b-versatile) |
| Python 3.11 | Programming language |

---

## 👤 Author

Made by **your name** — Data Science & AI Engineering Student

