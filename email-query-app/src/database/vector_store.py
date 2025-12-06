from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os

class EmailVectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        """Initialize vector store with HuggingFace embeddings."""
        self.embeddings = HuggingFaceEmbeddings()
        self.persist_directory = persist_directory
        self.vector_store = None

    def store_emails(self, emails, max_chars_per_email=2000):
        """
        Store emails in vector database.
        Truncates each email to max_chars_per_email to prevent token overflow.
        """
        docs = []
        for email_data in emails:
            content = email_data["content"][:max_chars_per_email]
            docs.append(
                Document(
                    page_content=f"Subject: {email_data['subject']}\nFrom: {email_data['sender']}\n\n{content}",
                    metadata={
                        "subject": email_data["subject"],
                        "sender": email_data["sender"],
                        "date": email_data["date"],
                        "id": email_data["id"]
                    }
                )
            )

        # Create or update Chroma vector store
        self.vector_store = Chroma.from_documents(
            docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()

    def get_retriever(self):
        """Return retriever for QA chain."""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Please store emails first.")
        return self.vector_store.as_retriever()
