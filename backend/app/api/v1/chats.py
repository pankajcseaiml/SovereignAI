from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.config import settings
from app.core.database import get_db
from app.models.conversation import Conversation
from app.worker import process_chat_task

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

manager = ConnectionManager()

@router.get("/")
async def get_chats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Conversation))
    conversations = result.scalars().all()
    return [{"id": c.id, "title": c.title} for c in conversations]

async def redis_listener(websocket: WebSocket, conversation_id: str):
    pubsub = redis_client.pubsub()
    channel = f"agent_progress_{conversation_id}"
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                await websocket.send_json(data)
    except Exception as e:
        print(f"Redis listener error: {e}")
    finally:
        await pubsub.unsubscribe(channel)

@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    await manager.connect(websocket)
    listener_task = asyncio.create_task(redis_listener(websocket, conversation_id))
    try:
        while True:
            data = await websocket.receive_text()
            # Dispatch to Celery to process the chat asynchronously
            process_chat_task.delay(conversation_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        listener_task.cancel()
