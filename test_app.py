import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_root():
    """Test the main page returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>FastAPI Chat</title>" in response.text

@pytest.mark.asyncio
async def test_websocket():
    """Test WebSocket send/receive"""
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello Test")
        # Since the server echoes to all clients including sender
        data = websocket.receive_text()
        assert data == "Hello Test"
