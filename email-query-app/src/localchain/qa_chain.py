import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

def query_emails(email_list: list[dict], query: str, date: str = "default") -> str:
    """
    Takes a list of email dicts and a natural language query,
    returns an AI-generated answer using Groq + LangChain.
    """

    # --- Step 1: Convert emails into text documents ---
    docs = []
    for email in email_list:
        content = f"Subject: {email.get('subject', '')}\nFrom: {email.get('from', '')}\n\n{email.get('body', '')}"
        docs.append(Document(page_content=content))

    # --- Step 2: Split into smaller chunks ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    # --- Step 3: Initialize embeddings ---
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # --- Step 4: Create or reuse local Chroma vectorstore ---
    persist_dir = os.path.join("data", f"emails_{date}")
    os.makedirs(persist_dir, exist_ok=True)
    vectordb = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir)

    # --- Step 5: Initialize Groq LLM ---
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("❌ GROQ_API_KEY missing in .env file")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key,
        temperature=0.3,
    )

    # --- Step 6: Create RetrievalQA chain ---
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=False,
    )

    # --- Step 7: Ask the question ---
    response = qa.run(query)
    return response or "No relevant information found."
