from base64 import urlsafe_b64encode, urlsafe_b64decode
from email.mime.text import MIMEText
from typing import List, Dict
import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core.crypto import decrypt


class GmailService:

    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    @staticmethod
    def get_gmail_client(agent):
        credentials = Credentials(
            token=None,
            refresh_token=decrypt(agent.refresh_token),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=agent.client_id,
            client_secret=decrypt(agent.client_secret),
            scopes=GmailService.SCOPES
        )

        return build("gmail", "v1", credentials=credentials)

    @staticmethod
    def extract_email_address(value: str) -> str:
        if not value:
            return ""

        match = re.search(r"<(.+?)>", value)
        if match:
            return match.group(1).strip()

        return value.strip()


    @staticmethod
    def clean_email_body(body: str) -> str:
        if not body:
            return ""

        patterns = [
            r"-----Original Message-----",
            r"On .* wrote:",
            r"Em .* escreveu:",
            r"From:.*",
            r"De:.*",
            r"Sent:.*",
            r"Enviado:.*",
            r"Subject:.*",
            r"Assunto:.*",
            r"To:.*",
            r"Para:.*",
            r"ARC-Seal:.*",
            r"DKIM-Signature:.*",
            r"Received:.*",
            r"Return-Path:.*",
            r"Authentication-Results:.*",
        ]

        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                body = body[:match.start()]

        return body.strip()

 
    @staticmethod
    def extract_email_body(message_data) -> str:
        payload = message_data.get("payload", {})

        def decode(data: str) -> str:
            try:
                return urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="ignore")
            except Exception:
                return ""

        body = ""

        # multipart
        if "parts" in payload:
            for part in payload["parts"]:
                mime_type = part.get("mimeType")
                data = part.get("body", {}).get("data")

                if mime_type == "text/plain" and data:
                    body = decode(data)
                    break

        # single part
        else:
            data = payload.get("body", {}).get("data")
            if data:
                body = decode(data)

        return GmailService.clean_email_body(body)

 
    @staticmethod
    def list_recent_emails(agent, limit: int = 5) -> List[Dict]:

        service = GmailService.get_gmail_client(agent)

        results = service.users().messages().list(
            userId="me",
            maxResults=limit
        ).execute()

        messages = results.get("messages", [])

        emails = []

        for msg in messages:
            data = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="full"
            ).execute()

            headers = data.get("payload", {}).get("headers", [])

            subject = ""
            sender = ""

            for h in headers:
                if h["name"] == "Subject":
                    subject = h["value"]
                if h["name"] == "From":
                    sender = h["value"]

            emails.append({
                "id": msg["id"],
                "sender": sender,
                "subject": subject,
                "body": GmailService.extract_email_body(data)
            })

        return emails

 
    @staticmethod
    def get_email_by_id(agent, message_id: str):

        service = GmailService.get_gmail_client(agent)

        data = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        headers = data.get("payload", {}).get("headers", [])

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        return {
            "id": message_id,
            "sender": sender,
            "sender_email": GmailService.extract_email_address(sender),
            "subject": subject,
            "body": GmailService.extract_email_body(data)
        }


    @staticmethod
    def send_email(agent, receiver: str, subject: str, body: str):

        try:
            service = GmailService.get_gmail_client(agent)

            receiver_clean = GmailService.extract_email_address(receiver)

            if not receiver_clean:
                raise Exception(f"Invalid receiver: {receiver}")

            message = MIMEText(body, "plain", "utf-8")
            message["To"] = receiver_clean
            message["Subject"] = subject

            raw_message = urlsafe_b64encode(
                message.as_bytes()
            ).decode("utf-8")

            sent = service.users().messages().send(
                userId="me",
                body={"raw": raw_message}
            ).execute()

            return {
                "message_id": sent["id"],
                "status": "sent"
            }

        except HttpError as error:
            raise Exception(f"Gmail error: {error}")