from google_auth_oauthlib.flow import InstalledAppFlow
import os

# ---- CONFIG ----
CREDS_PATH = "last.json"        # your OAuth client credentials from Google Cloud
TOKEN_PATH = "token.json"       # will be created automatically
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def run_gmail_auth():
    if not os.path.exists(CREDS_PATH):
        raise FileNotFoundError(f"❌ '{CREDS_PATH}' not found. Make sure your OAuth client secret JSON is in place.")

    print("🔐 Launching Gmail OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)

    # Use localhost (browser-based) auth flow — opens Google sign-in window
    creds = flow.run_local_server(port=8502, prompt='consent')

    # Save token
    with open(TOKEN_PATH, "w") as token:
        token.write(creds.to_json())

    print(f"✅ Token saved successfully at: {TOKEN_PATH}")
    print("🎉 Gmail authentication complete!")

if __name__ == "__main__":
    run_gmail_auth()
