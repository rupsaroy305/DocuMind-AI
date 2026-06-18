# DocuMind AI

**RAG-powered Document Intelligence System** that allows you to upload PDFs and ask context-aware questions with fast, accurate answers using **Groq + FAISS + LangChain**.

---

## 🚀 Live Demo
https://docu-ai-system.streamlit.app/

---

##  Overview

**DocuMind AI** is a Retrieval-Augmented Generation (**RAG**) system that transforms any PDF into an interactive AI-powered knowledge assistant.

It enables users to:
-  Upload PDF documents
-  Ask natural language questions
-  Get context-aware answers grounded in the document
-  Retrieve information in seconds using AI

---

##  Features

-  **PDF Upload & Processing**
-  **RAG-based Question Answering**
-  **Semantic Search using FAISS**
-  **Fast inference using Groq API**
-  **Chat-style Streamlit UI**
-  **Context-grounded responses (no hallucinations outside document)**

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| LLM API | Groq (LLaMA 3 / Mixtral) |
| Embeddings | sentence-transformers |
| Vector Database | FAISS |
| Framework | LangChain |
| PDF Parsing | PyPDF |

---

##  How It Works

1.  **Upload PDF document**
2.  **Text is split into chunks**
3.  **Embeddings are generated**
4.  **FAISS stores vector representations**
5.  **User query retrieves relevant chunks**
6.  **Groq LLM generates final answer using context**

