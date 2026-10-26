# Local RAG PDF Assistant with Conversational Memory

An enterprise-grade, cost-optimized Retrieval-Augmented Generation (RAG) CLI application built using Python, LangChain, Chroma DB, and HuggingFace local embeddings. 

This project demonstrates an efficient approach to document querying by utilizing local embedding generation to reduce API overhead, combined with a persistent vector store and a conversational memory chain that handles context-aware follow-up questions.

---

## 🌟 Key Architecture & Features

- **Modern LCEL (LangChain Expression Language):** Built entirely on modern LangChain patterns to avoid legacy deprecation issues.
- **Cost-Optimized Hybrid Embeddings:** Uses local HuggingFace embeddings (`sentence-transformers/all-MiniLM-L6-v2`) for vector generation, eliminating vector storage embedding costs and protecting data privacy.
- **Persistent Local Vector Storage:** Utilizes **Chroma DB** to persist vector embeddings locally, preventing the need to re-index documents on every script execution.
- **Conversational Memory & Contextualization:** Features a history-aware retriever that rephrases ambiguous follow-up questions into standalone queries based on chat history.
- **Secure Configuration:** Separates sensitive API credentials using environment variables (`.env`).

---

## 🛠️ Tech Stack

- **Language:** Python 3.13+
- **Orchestration:** LangChain, LangChain Core, LangChain Chroma, LangChain HuggingFace
- **Vector Database:** Chroma DB (Local Persistent)
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **LLM:** OpenAI-compatible API (configured via Yantra API / custom base URL)

---

## 📁 Project Structure

```text
rag-pdf-assistant/
│
├── project.py          # Main execution script containing RAG pipeline & CLI loop
├── requirements.txt    # Pinned production dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Excludes sensitive keys, virtualenvs, and local DBs
└── constitution.pdf    # Target document processed by the pipeline
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/rag-pdf-assistant.git
cd rag-pdf-assistant
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory based on `.env.example`:
```env
YANTRA_API_KEY=your_actual_api_key_here
YANTRA_BASE_URL=your_actual_base_url_here
```

### 5. Run the Application
Ensure your target document (`constitution.pdf`) is placed in the project directory, then run:
```bash
python project.py
```

---

## 💡 Example Usage Flow
```text
Loading c:\lang\constitution.pdf...
Aapke data mein 19 pages hain.
Total chunks ban gaye: 241
⏳ Local HuggingFace Embeddings load ho rahi hain...
📁 Purana Chroma DB './chroma_db' mil gaya, load kiya ja raha hai...

✅ Setup poora ho gaya hai! Ab aap apne sawal pooch sakte hain. (Band karne ke liye 'exit' likhein)

Aapka Sawal: What are the fundamental rights?
⏳ AI aapke sawal ka jawab dhoondh raha hai, thoda wait karein...
🤖 Jawab:
[Generated response based on document context]

Aapka Sawal: Explain the third one in simple words.
⏳ AI aapke sawal ka jawab dhoondh raha hai, thoda wait karein...
🤖 Jawab:
[Context-aware response utilizing conversation memory]
```

---

## 🛡️ Security & Best Practices
- **No Hardcoded Secrets:** All API keys and endpoints are externalized via `.env`.
- **Ignored Artifacts:** Local vector databases (`chroma_db/`), virtual environments, and log caches are explicitly ignored via `.gitignore` to keep the repository clean and secure.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).