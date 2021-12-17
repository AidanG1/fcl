from fastapi import APIRouter, HTTPException
from ..main import project_key, db_prefix, create_update_rating_week
from ..models import Player
from deta import Deta
import datetime

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


'''
name: str  # Magnus Carlsen
title_full: Optional[str] = ''  # Grandmaster
title_abbreviated: Optional[str] = ''  # GM
# https://ratings.fide.com/profile/1503014
fide_id: str
# https://lichess.org/@/DrNykterstein
lichess_username: Optional[str] = None
# https://www.chess.com/member/magnuscarlsen
chess_com_username: Optional[str] = None
# https://www.365chess.com/players/Magnus_carlsen
chess_365_username: Optional[str] = None
# https://www.youtube.com/channel/UCbdcpQ5uPPymv7Ea0nnFfOw
youtube_channel: Optional[str] = None
# https://www.twitch.tv/magnuscarlsentv
twitch_channel: Optional[str] = None
honors: Optional[List[str]] = None
birth_year: Optional[int] = None  # 1990
birth_country: Optional[str] = None  # Norway
image_url: Optional[str] = None
'''

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
        create_update_rating_week(player)
        return player
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if player is None:
        raise HTTPException(
            status_code=404, detail="Data must be added to create a player")
