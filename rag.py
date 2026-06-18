import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def load_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    return loader.load()


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(documents)


def create_vector_store(pdf_path: str):
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_qa_chain(vectorstore):

    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=1024,
    )

    prompt = PromptTemplate.from_template("""You are a helpful AI study assistant.

Use the following context from the uploaded document to answer the student's question.

If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {question}

Answer:""")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_context(question):
        docs = retriever.invoke(question)
        return format_docs(docs)

    chain = (
        {
            "context": lambda x: get_context(x["question"]),
            "question": lambda x: x["question"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain