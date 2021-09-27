from modules import Database, ConnectionManager
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
import json
import uvicorn

app = FastAPI()
app.mount("/caro", StaticFiles(directory="static"))
USER_PASS = "19TCLC_DT6"
ADMIN_PASS = "batnapquantaihonemlancuoi"

manager = ConnectionManager.ConnectionManager()
db = Database.Database("data.json")


@app.get("/{every_thing}")
async def not_found(every_thing:str):
    return RedirectResponse("https://www.facebook.com/huytuong010101/")


@app.websocket("/ws/{password}")
async def websocket_endpoint(websocket: WebSocket, password: str):
    if password != USER_PASS:
        print("Client wrong password:", password)
        return
    await manager.connect(websocket)
    await websocket.send_json(db.data)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/admin/{password}")
async def websocket_endpoint(websocket: WebSocket, password: str):
    if password != ADMIN_PASS:
        print("Admin wrong password:", password)
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
