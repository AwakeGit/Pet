from application.commands import get_history, websocket_endpoint
from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.get("/notifications/history/{user_id}")
async def get_history_endpoint(user_id: str):
    return await get_history(user_id)


@router.websocket("/ws/notifications")
async def websocket_endpoint_ws(websocket: WebSocket):
    await websocket_endpoint(websocket)
