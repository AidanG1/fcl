from fastapi import APIRouter, HTTPException
from ..main import project_key, db_prefix
from ..models import Player
from deta import Deta

router = APIRouter()

bidirectional_titles = {
    'GM': 'Grandmaster',
    'IM': 'International Master',
    'FM': 'FIDE Master',
    'CM': 'Candidate Master',
    'WGM': 'Woman Grandmaster',
    'WIM': 'Woman International Master',
    'WFM': 'Woman FIDE Master',
    'WCM': 'Woman Candidate Master',
}
revd = dict([reversed(i) for i in bidirectional_titles.items()])
bidirectional_titles.update(revd)


@router.get("/players/{player_key}", response_model=Player, tags=["players"])
async def read_user_by_id(player_key: str):
    deta = Deta(project_key)
    db = deta.Base(db_prefix+'players')
    try:
        player = db.get(key=player_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if player is None:
        raise HTTPException(
            status_code=404, detail="The player doesn't exist")
    return player


@router.post("/players/post")
async def create_player(player: Player):
    deta = Deta(project_key)
    db = deta.Base(db_prefix+'players')
    try:
        if player.title_abbreviated == '' and player.title_full != '':
            player.title_abbreviated = bidirectional_titles[player.title_full]
        elif player.title_abbreviated != '' and player.title_full == '':
            player.title_full = bidirectional_titles[player.title_abbreviated]
        player = db.insert(player)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if player is None:
        raise HTTPException(
            status_code=404, detail="The player doesn't exist")
