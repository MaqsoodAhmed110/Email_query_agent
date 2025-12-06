import base64
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup  # ✅ For HTML parsing

class GmailClient:
    def __init__(self, creds_path, token_path):
        self.creds_path = creds_path
        self.token_path = token_path
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate and return a Gmail API service instance."""
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path)
        else:
            raise Exception(f"Token file not found at {self.token_path}. Run Gmail OAuth flow first.")
        service = build('gmail', 'v1', credentials=creds)
        print("🔑 Gmail authentication successful!")
        return service

    def get_emails_by_date(self, date_str):
        """Fetch all emails from Gmail for a specific date."""
        try:
            selected_date = datetime.strptime(date_str, "%Y/%m/%d")
            next_day = selected_date + timedelta(days=1)

            after = selected_date.strftime("%Y/%m/%d")
            before = next_day.strftime("%Y/%m/%d")
            query = f"after:{after} before:{before}"
            print(f"📅 Fetching emails from: {after} to {before}")

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=50
            ).execute()

            messages = results.get('messages', [])
            emails = []

            if not messages:
                print("📭 No emails found for this date.")
                return emails

            for msg in messages:
                msg_detail = self.service.users().messages().get(userId='me', id=msg['id']).execute()

                payload = msg_detail.get('payload', {})
                headers = payload.get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')

                # Extract body
                body_text = ""
                parts = payload.get('parts', [])
                if parts:
                    for part in parts:
                        if part['mimeType'] in ['text/plain', 'text/html']:
                            data = part['body'].get('data')
                            if data:
                                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                                if part['mimeType'] == 'text/html':
                                    soup = BeautifulSoup(decoded_data, 'html.parser')
                                    decoded_data = soup.get_text()
                                body_text += decoded_data + "\n"
                else:
                    body_data = payload.get('body', {}).get('data', '')
                    if body_data:
                        decoded_body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                        soup = BeautifulSoup(decoded_body, 'html.parser')
                        body_text = soup.get_text()

                emails.append({
                    "subject": subject.strip(),
                    "from": sender.strip(),
                    "body": body_text.strip()
                })

                print(f"📩 Email: {subject} | From: {sender}")
                print("-" * 80)

            return emails

        except Exception as e:
            print(f"❌ Error while fetching emails: {e}")
            return []
