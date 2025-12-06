import streamlit as st
from dotenv import load_dotenv
import os
from localchain.qa_chain import query_emails
from email_utils.gmail_client import GmailClient

# Load environment variables (optional)
load_dotenv()

# File paths
CREDS_PATH = os.path.join("last.json")
TOKEN_PATH = os.path.join("token.json")

# Streamlit UI
st.set_page_config(page_title="📧 Gmail Email Query Assistant", page_icon="🤖")

st.title("📧 Gmail Email Query Assistant")
st.write("Ask questions about your Gmail emails for a specific date using LangChain + Groq!")

# Initialize Gmail client
if not os.path.exists(TOKEN_PATH):
    st.error("❌ token.json not found. Please run Gmail OAuth first (setup_gmail_auth.py).")
else:
    gmail_client = GmailClient(CREDS_PATH, TOKEN_PATH)
    st.success("✅ Gmail connected successfully!")

    # Date input
    date_str = st.text_input("Enter date (YYYY/MM/DD):", "")

    if st.button("Fetch Emails"):
        if not date_str:
            st.warning("Please enter a valid date first.")
        else:
            emails = gmail_client.get_emails_by_date(date_str)
            if not emails:
                st.info("📭 No emails found for this date.")
            else:
                st.session_state["emails"] = emails
                st.success(f"✅ Fetched {len(emails)} emails for {date_str}")

# Show fetched emails
if "emails" in st.session_state:
    st.subheader("Fetched Emails:")
    for idx, email in enumerate(st.session_state["emails"]):
        with st.expander(f"{idx+1}. {email['subject']} (from {email['from']})"):
            st.text_area("Body", email["body"], height=150)

# Question input
user_query = st.text_input("💬 Ask a question about these emails:")
if st.button("Ask AI"):
    if "emails" not in st.session_state or not st.session_state["emails"]:
        st.warning("Please fetch some emails first.")
    elif not user_query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            result = query_emails(st.session_state["emails"], user_query)
            st.success("✅ Answer ready:")
            st.write(result)
