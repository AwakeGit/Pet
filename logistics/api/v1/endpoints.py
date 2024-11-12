from application.commands import update_status
from domain.models import StatusUpdate
from fastapi import APIRouter

router = APIRouter()


@router.post("/logistics/update")
async def update_status_endpoint(update: StatusUpdate):
    return await update_status(update)
