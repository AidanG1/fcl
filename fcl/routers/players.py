from fastapi import APIRouter, HTTPException
from ..main import project_key, db_prefix
from ..models import Player
from deta import Deta

router = APIRouter()


@router.get("/players/{player_id}", response_model=Player, tags=["players"])
async def read_user_by_id(player_id: str):
    deta = Deta(project_key)
    db = deta.Base(db_prefix+'players')
    try:
        player = db.get(key=player_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if player is None:
        raise HTTPException(
            status_code=404, detail="The player doesn't exist")
    return player