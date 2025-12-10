from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
  <head>
    <title>FastAPI Chat</title>
  </head>
  <body>
    <h1>Real-time Chat</h1>

    <ul id="messages"></ul>

    <input id="messageInput" autocomplete="off" placeholder="Type a message"/>
    <button onclick="sendMessage()">Send</button>

    <script>
      // Correct WebSocket URL for Docker or localhost
      var ws = new WebSocket("ws://" + window.location.host + "/ws");

      ws.onmessage = function(event) {
        var messages = document.getElementById("messages");
        var li = document.createElement("li");
        li.textContent = event.data;
        messages.appendChild(li);
      };

      function sendMessage() {
        var input = document.getElementById("messageInput");
        if (input.value.trim() !== "") {
          ws.send(input.value);
          input.value = "";
        }
      }
    </script>
  </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

# List of connected clients
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            # Send message to ALL clients including sender
            for client in clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(websocket)
