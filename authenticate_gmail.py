# filename: authenticate_gmail.py
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# This scope gives full Gmail access — for cleaning use.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    creds = None
    # If token.json exists, reuse it.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Otherwise, do OAuth flow.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the token.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

if __name__ == '__main__':
    main()
