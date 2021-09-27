import datetime
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import uvicorn

app = FastAPI()
app.mount("/caro", StaticFiles(directory="templates"))
USER_PASS = "123"
ADMIN_PASS = "321"


class Database:
    def __init__(self):
        with open("data.json", encoding="utf-8") as f:
            self.data = json.loads(f.read())

    def add(self, win: str, lose: str, time=str(datetime.datetime.now())):
        self.data.append([win, lose, time])
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f)

    def remove(self, win: str, lose: str):
        for i in range(len(self.data) - 1, -1, -1):
            if self.data[i][0] == win and self.data[i][1] == lose:
                del self.data[i]
                break
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()
db = Database()


@app.websocket("/ws/{password}")
async def websocket_endpoint(websocket: WebSocket, password: str):
    if password != USER_PASS:
        return
    await manager.connect(websocket)
    await websocket.send_json(db.data)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/admin/{password}")
async def websocket_endpoint(websocket: WebSocket, password: str):
    if password != ADMIN_PASS:
        return
    await manager.connect(websocket)
    await websocket.send_json(db.data)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if data["type"] == "add":
                db.add(data["win"], data["lose"])
                await manager.broadcast(db.data)
            elif data["type"] == "remove":
                db.remove(data["win"], data["lose"])
                await manager.broadcast(db.data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
