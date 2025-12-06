# Email Query Agent (LangChain + Groq)

Simple app to fetch a user's Gmail messages for a selected date, index them into a vector DB, and answer natural-language questions using LangChain + Groq. Built with Streamlit for the UI.

## Features
- OAuth2 sign-in to Gmail
- Fetch all emails from a selected day
- Convert emails to LangChain Documents and embed them
- Store embeddings in Chroma (or FAISS)
- Use LangChain RetrievalQA with Groq LLM to answer queries
- Streamlit UI for date selection and Q&A

## Prerequisites
- Windows machine
- Python 3.10+ (adjust if your environment requires different version)
- Google Cloud project with Gmail API enabled
- Groq API key

## Files to configure
- `credentials.json` — Google OAuth 2.0 credentials (save at project root or `src/` as used by your code)
- `.env` — environment variables (do NOT commit)
  - Example:
    - GROQ_API_KEY=your-groq-api-key
    - GOOGLE_CLIENT_ID=your-client-id
    - GOOGLE_CLIENT_SECRET=your-client-secret

## Setup (Windows)
1. Open PowerShell in project folder:
   cd "C:\Users\user\Desktop\Agentic\email-query-app"

2. Create & activate virtual environment:
   - Create:
     python -m venv .venv
   - Activate:
     .\.venv\Scripts\Activate.ps1
     (or use `.\.venv\Scripts\activate` in cmd)

3. Install dependencies:
   pip install -r requirements.txt

4. Place Google OAuth credentials:
   - In Google Cloud Console:
     - Enable Gmail API
     - OAuth consent screen configured
     - Create OAuth Client ID (Desktop) and download `credentials.json`
   - Put `credentials.json` in project root (or `src/` if your code expects it there)

5. Add secrets to `.env`:
   - Fill GROQ_API_KEY and optionally GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET if your flow reads them from env

## Running the app
First Run:
python setup_gmail_auth.py


Run Streamlit (default port 8501):
streamlit run src/app.py

If you need a specific port:
streamlit run src/app.py --server.port 8501

Open the URL shown in the terminal, typically:
http://localhost:8501

During first Gmail sign-in the OAuth flow will open a browser window and create `token.pickle` (or similar) locally to persist tokens.

## Notes & Troubleshooting
- Keep `.env` and `credentials.json` out of source control. `.gitignore` in repo already excludes them.
- If port 8501 is used, Streamlit will try the next free port (8502, ...). You can force a port with `--server.port`.
- The Google OAuth client type "Desktop" allows the local server flow; you generally do not need to add redirect URIs for desktop clients.
- If authentication fails, delete `token.pickle` and re-run to re-initiate auth.
- If using Chroma, ensure you configure persistent directory if you want persistence across runs.
- For Groq model changes, update the LangChain LLM initialization in your code and ensure GROQ_API_KEY is set.

## Development tips
- Add unit tests for email parsing and vector-store logic.
- Log message counts and any failures when fetching/parsing emails.
- Limit email fetch scope during testing (use a narrow date with few messages).

## License
Use / adapt as needed for your assignment. Do not share credentials publicly.
