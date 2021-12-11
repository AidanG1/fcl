from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from deta import Deta, App
import os
import requests
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
project_key = os.getenv("PROJECT_KEY")
if os.getenv('DETA_RUNTIME') == 'true':
    db_prefix = 'fcl_prod_'
else:
    db_prefix = 'fcl_dev_'

app = App(FastAPI())

# deta update -e .env
# deta cron set "10 minutes"


@app.lib.cron()
def cron_job(event):
    deta = Deta(project_key)
    db = deta.Base(db_prefix+'players')
    players = db.fetch().items
    for player in players:
        r = requests.get()  # hit the chess.com api and then the lichess api
        # scrape the fide website for ratings or maybe chess.com/players
        # eventually go for finding fide games
        # then make a new rating_day
        # also scrape from the youtube api and from a twitch api to get that data

    return "this is not done"


class Player(BaseModel):
    id: int
    name: str
    title: str
    fide_id: str
    lichess_username: Optional[str] = None
    chess_com_player_username: Optional[str] = None
    chess_com_username: Optional[str] = None
    youtube_channel: Optional[str] = None
    twitch_channel: Optional[str] = None
    honors: Optional[List[str]] = None
    birth_year: Optional[int] = None
    birth_country: Optional[str] = None
    image_url: Optional[str] = None

# need to figure out what players deserve to earn points for hmmmmmmmmmm


class Rating_day(BaseModel):  # https://www.chess.com/games/daniel-naroditsky
    id: int
    day: datetime.date
    fide_classical: int
    fide_rapid: int
    fide_blitz: int
    lichess_ratings: List[int]  # classical, rapid, blitz, bullet
    chess_com_ratings: List[int]  # classical, rapid, blitz, bullet
    lichess_games_played: List[int]  # classical, rapid, blitz, bullet
    chess_com_games_played: List[int]  # classical, rapid, blitz, bullet
    # https://lichess.org/api#operation/apiGamesUser


class Daily_fantasy_instance(BaseModel):
    id: int
    player_id: int


class League(BaseModel):
    id: int
    teams: List[int]
    league_name: str


class Team(BaseModel):
    id: int
    players: List[str]


router = APIRouter()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/players/{player_id}", response_model=Player, tags=["database"])
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
