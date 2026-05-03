# 📄 PDF Semantic Search Engine — REST API

A FastAPI-based REST API that allows users to **upload PDF files** and perform **semantic search** on their content using HuggingFace embeddings and Qdrant vector database.

---

## 🚀 Features

- 📤 Upload PDF files via REST API
- 🧠 Automatically extract and chunk text from PDFs
- 🔢 Generate semantic embeddings using HuggingFace (`all-MiniLM-L6-v2`)
- 🗄️ Store embeddings in Qdrant vector database
- 🔍 Perform semantic similarity search with ranked results
- ⚡ Built with FastAPI for high performance

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | REST API framework |
| **Qdrant** | Vector database for storing embeddings |
| **HuggingFace** | Embedding model (`all-MiniLM-L6-v2`) |
| **LangChain** | HuggingFace embeddings integration |
| **PyPDF** | PDF text extraction |
| **Uvicorn** | ASGI server |
| **Python-dotenv** | Environment variable management |

---

## 📁 Project Structure

```
PDF_Search_Engine/
│
├── main.py          # FastAPI app entry point
├── route.py         # API endpoints (upload PDF, search query)
├── model.py         # Text chunking and embedding logic
├── vector_db.py     # Qdrant database setup
├── uploads/         # Uploaded PDF files (auto-created)
├── qdrant_storage/  # Local Qdrant vector storage (auto-created)
├── .env             # Environment variables
└── README.md        # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/pdf-semantic-search.git
cd pdf-semantic-search
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn pypdf python-dotenv qdrant-client langchain-huggingface sentence-transformers
```

### 4. Create `.env` File
```env
# Add your environment variables here if needed
```

---

## ▶️ Running the API

```bash
python main.py
```

Server will start at:
```
http://127.0.0.1:8000
```

Interactive API docs available at:
```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 1. Upload PDF

| Property | Value |
|----------|-------|
| **Method** | `POST` |
| **Endpoint** | `/pdf/Upload_PDF_Here` |
| **Input** | PDF file (multipart/form-data) |

**Example using cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/pdf/Upload_PDF_Here" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

**Success Response:**
```json
{
  "message": "PDF 'your_document.pdf' uploaded and indexed successfully.",
  "chunks": 42
}
```

**Error Response:**
```json
{
  "detail": "Only PDF files are allowed."
}
```

---

### 2. Semantic Search

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/pdf/query/{query}` |
| **Input** | Query string in URL |

**Example using cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/pdf/query/What is machine learning?"
```

**Success Response:**
```json
{
  "results": [
    {
      "rank": 1,
      "score": 0.91,
      "text": "Machine learning is a subset of artificial intelligence...",
      "file": "your_document.pdf"
    },
    {
      "rank": 2,
      "score": 0.87,
      "text": "Supervised learning algorithms learn from labeled data...",
      "file": "your_document.pdf"
    }
  ]
}
```

**No Results Response:**
```json
{
  "message": "No Relevant Answer found!"
}
```

---

## 🔄 How It Works

```
User uploads PDF
       ↓
Text extracted from PDF (PyPDF)
       ↓
Text split into chunks (500 words each)
       ↓
Chunks converted to vectors (HuggingFace all-MiniLM-L6-v2)
       ↓
Vectors stored in Qdrant with metadata
       ↓
User sends search query
       ↓
Query converted to vector
       ↓
Qdrant finds top 5 similar vectors (Cosine Similarity)
       ↓
Ranked results returned to user
```

---

## 🧪 Testing with Swagger UI

1. Open browser and go to `http://127.0.0.1:8000/docs`
2. Click on `POST /pdf/Upload_PDF_Here` → **Try it out** → Upload your PDF → **Execute**
3. Click on `GET /pdf/query/{query}` → **Try it out** → Enter your query → **Execute**

---

## 📦 Dependencies

```txt
fastapi
uvicorn
pypdf
python-dotenv
qdrant-client
langchain-huggingface
sentence-transformers
```

Install all at once:
```bash
pip install fastapi uvicorn pypdf python-dotenv qdrant-client langchain-huggingface sentence-transformers
```

---

## ⚠️ Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `400 Bad Request` | Non-PDF file uploaded | Upload only `.pdf` files |
| `500 Internal Server Error` | Qdrant connection failed | Check `qdrant_storage` folder permissions |
| `422 Unprocessable Entity` | Wrong input format | Check your request format |
| `405 Method Not Allowed` | Wrong HTTP method used | Use correct method (GET/POST) |

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)

---

## 📜 License

This project is licensed under the **MIT License**.
