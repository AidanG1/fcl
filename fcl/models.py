from pydantic import BaseModel
from typing import List, Optional
import datetime


class Player(BaseModel):
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

# need to figure out what players deserve to earn points for hmmmmmmmmmm


class Opening(BaseModel):
    opening_name: str
    opening_color: str
    opening_first_move: str


class Rating_week(BaseModel):  # https://www.chess.com/games/daniel-naroditsky
    player: Player
    week_number: int  # makes it easier to get previous data to compare
    start_day: datetime.date
    end_day: datetime.date  # start_day + 6 to make a 1 week period
    fide_classical: int
    fide_rapid: int
    fide_blitz: int
    lichess_ratings: List[int] = []  # classical, rapid, blitz, bullet
    chess_com_ratings: List[int] = []  # classical, rapid, blitz, bullet
    fide_games_played: List[int] = []  # classical, rapid, blitz
    lichess_games_played: List[int] = []  # classical, rapid, blitz, bullet
    chess_com_games_played: List[int] = []  # classical, rapid, blitz, bullet
    classical_openings: List[Opening] = []
    rapid_openings: List[Opening] = []
    blitz_openings: List[Opening] = []
    bullet_openings: List[Opening] = []
    youtube_subs: Optional[int]
    youtube_views: Optional[int]
    # https://twitchstats.net/streamer/magnuscarlsentv
    twitch_average_viewers: Optional[int]
    twitch_total_viewers: Optional[int]
    # https://lichess.org/api#operation/apiGamesUser


class User(BaseModel):
    username: str


class League(BaseModel):
    league_name: str
    league_description: str = ''
    league_size_limit: int = 10
    fide_multiplier: float = 2  # multiplier
    lichess_chess_multiplier: float = 1
    classical_multiplier: float = 12
    rapid_multiplier: float = 6
    blitz_multiplier: float = 3
    bullet_multiplier: float = 1
    opening_bonus_multiplier: float = 2


class Team(BaseModel):
    owner: User
    league: League
    name: str
    players: List[Player]
    starting: List[Player]
    not_starting: List[Player]
    opening_bonus_selection: Optional[Opening]
    weekly_placements: List[int]  # lower number is better
    weekly_points: List[float]  # last items in list are most recent


class Trade(BaseModel):
    date: datetime.date
    team1: Team
    team2: Team
    players1: List[Player]
    players2: List[Player]


class FreeAgency(BaseModel):
    date: datetime.date
    team: Team
    player_pickup: Player
    player_drop: Player
