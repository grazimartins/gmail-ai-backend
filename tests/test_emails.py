from unittest.mock import patch
import uuid

def create_test_agent(client):

    unique_email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"

    payload = {
        "name": "Email Agent",
        "email_gmail": unique_email,
        "client_id": "client-id",
        "client_secret": "client-secret",
        "refresh_token": "refresh-token"
    }

    response = client.post(
        "/agents",
        json=payload
    )

    return response.json()["id"]


@patch("app.services.ai_service.AIService.summarize_email")
@patch("app.services.gmail_service.GmailService.send_email")
@patch("app.services.gmail_service.GmailService.get_email_by_id")
def test_summarize_and_forward(
    mock_get_email,
    mock_send_email,
    mock_summarize,
    client
):

    agent_id = create_test_agent(client)

    mock_get_email.return_value = {
        "id": "1",
        "subject": "Test Email",
        "body": "Hello, can you help me?",
        "sender_email": "google@gmail.com"
    }
    
    mock_summarize.return_value = "AI Summary"

    mock_send_email.return_value = {
        "message_id": "999"
    }

    payload = {
        "agent_id": agent_id,
        "message_id": "123",
        "forward_to": "manager@gmail.com"
    }

    response = client.post(
        "/emails/summarize-and-forward",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"] == "AI Summary"


@patch("app.services.ai_service.AIService.generate_email_reply")
@patch("app.services.gmail_service.GmailService.send_email")
@patch("app.services.gmail_service.GmailService.get_email_by_id")
def test_auto_reply(
    mock_get_email,
    mock_send_email,
    mock_generate_reply,
    client
):

    agent_id = create_test_agent(client)

    mock_get_email.return_value = {
        "id": "1",
        "subject": "Test Email",
        "body": "Hello, can you help me?",
        "sender_email": "google@gmail.com"
    }

    mock_generate_reply.return_value = "Sure, I can help you."

    mock_send_email.return_value = {
        "message_id": "888"
    }

    payload = {
        "agent_id": agent_id,
        "message_id": "321"
    }

    response = client.post(
        "/emails/auto-reply",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reply"] == "Sure, I can help you."