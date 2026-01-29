📄 Ask Your PDF
Chat with Documents using Local AI (Nebula AI • Neural PDF Engine)

Ask Your PDF is a local AI-powered PDF question answering system that allows users to upload a PDF and interact with it conversationally.
All answers are strictly grounded in the uploaded document using semantic search and a local LLM (Ollama).

✨ Features

📤 Upload PDF directly from the web interface

💬 Chat with your document in natural language

🧠 Semantic search using FAISS + Sentence Transformers

🤖 Local LLM inference via Ollama (no cloud APIs)

⚡ Real-time streaming responses (token-by-token)

🔒 Fully local & privacy-friendly

🎨 Modern glassmorphism UI (Nebula AI theme)

🧩 Architecture Overview
PDF Upload
   ↓
Text Extraction (pdf_loader.py)
   ↓
Chunking (qa_engine.py)
   ↓
Embeddings (SentenceTransformers)
   ↓
Vector Search (FAISS)
   ↓
Context Injection (RAG)
   ↓
Local LLM (Ollama)
   ↓
Streaming Response (Flask + JS)

🛠️ Tech Stack

Backend

Python

Flask

FAISS

Sentence-Transformers

Ollama (LLM runtime)

Frontend

HTML5

CSS3 (Glassmorphism UI)

JavaScript (Streaming Fetch API)

🚀 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/ask-your-pdf.git
cd ask-your-pdf

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate     # Linux / Mac
venv\Scripts\activate        # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install & run Ollama

Download Ollama from:
👉 https://ollama.com

Pull a lightweight model:

ollama pull llama3


⚠️ If you have low RAM, use a smaller model like:

ollama pull mistral

5️⃣ Start the application
python app.py


Open your browser at:

http://127.0.0.1:5000

🧪 How to Use

Upload a PDF using the Upload PDF button

Wait for the document to be processed

Ask questions like:

What is this document about?

Show total amount

List all dates

Summarize the document

Get real-time, grounded answers ✨

📌 Example Questions

What is the grand total amount?

What happens on 19 FEB 2026?

List all events and dates

Explain the document in simple terms

Summarize the quotation

🔐 Privacy & Security

No external APIs

No cloud storage

Documents never leave your system

Runs entirely on localhost

🧠 Future Enhancements

📚 Multi-PDF support

📄 Page-level citations

🖍 Highlight answers in PDF

🌙 Dark/Light mode toggle

🔍 Search inside tables

👥 User sessions. <img width="1365" height="585" alt="Screenshot 2026-01-29 122655" src="https://github.com/user-attachments/assets/f1bbe47f-adf4-4a58-a0df-9acac2696648" />
