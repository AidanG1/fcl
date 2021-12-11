from pydantic import BaseModel
from typing import List, Optional
import datetime


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
