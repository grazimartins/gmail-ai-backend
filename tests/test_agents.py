from fastapi.testclient import TestClient
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



def test_create_agent_invalid_email(client):

    payload = {
        "name": "Test Agent",
        "email_gmail": "invalid-email",
        "client_id": "client-id",
        "client_secret": "client-secret",
        "refresh_token": "refresh-token"
    }

    response = client.post(
        "/agents",
        json=payload
    )

    assert response.status_code == 422