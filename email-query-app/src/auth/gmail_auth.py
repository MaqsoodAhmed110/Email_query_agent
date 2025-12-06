import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail read-only scope
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_credentials():
    """Authenticate and return Gmail API credentials."""
    creds = None

    # Base directory (one level up from this file)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    creds_path = os.path.join(base_dir, "last.json")
    token_path = os.path.join(base_dir, "token.json")

    print(f"🔍 Looking for credentials at: {creds_path}")
    print(f"📦 Token will be stored at: {token_path}")

    # Check for existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If no valid credentials, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("♻️ Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"❌ credentials.json not found at: {creds_path}")

            print("🌐 Launching browser for Google sign-in...")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)

            # IMPORTANT: Port must match one of the redirect URIs in Google Cloud Console
            creds = flow.run_local_server(port=8502, prompt="consent")

        # Save the new token for next time
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
            print(f"✅ Token saved successfully to: {token_path}")

    print("🔑 Gmail authentication successful!")
    return creds
