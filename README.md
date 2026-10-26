# Local RAG PDF Assistant with Conversational Memory

A robust, cost-optimized, command-line Retrieval-Augmented Generation (RAG) application built with Python and LangChain. It allows users to query PDF documents locally with persistent vector storage and contextual conversation memory for seamless follow-up questions.

---

## 🚀 Key Features

* **Modern LCEL Architecture:** Built using pure LangChain Expression Language (LCEL) to avoid legacy module deprecation issues.
* **Cost-Optimized Hybrid Approach:** Utilizes local HuggingFace embeddings (`all-MiniLM-L6-v2`) to save API costs and protect data privacy, paired with a cloud-based LLM.
* **Persistent Vector Storage:** Automatically stores and loads vector embeddings locally using **Chroma DB**, avoiding redundant processing.
* **Conversational Memory:** Implements context-aware history rephrasing so you can ask natural follow-up questions (e.g., *"Explain the second one"*).

---

## 🛠️ Tech Stack

* **Language:** Python 3.13
* **Orchestration:** LangChain, LangChain Core, LangChain Community
* **Vector Database:** Chroma DB
* **Embeddings:** HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
* **LLM:** OpenAI-compatible API (configured via Yantra API / `gpt-4o-mini`)

---

## 📂 Project Structure

```text
├── project.py         # Main RAG execution script
├── requirements.txt   # Python dependencies
├── .env.example       # Template for environment variables
├── .gitignore         # Files and folders ignored by Git
└── constitution.pdf   # Target document for RAG querying
