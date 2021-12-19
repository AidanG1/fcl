from fastapi import FastAPI, APIRouter, HTTPException, status
from deta import Deta, App
from models import *
from bs4 import BeautifulSoup
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from .routers import players


load_dotenv()
project_key = os.getenv("PROJECT_KEY")
if os.getenv('DETA_RUNTIME') == 'true':
    db_prefix = 'fcl_prod_'
else:
    db_prefix = 'fcl_dev_'

app = FastAPI()
app.include_router(players)
app = App(app)
# deta update -e .env
# deta cron set "10 minutes"


def create_update_rating_week(players):
    """
    Inputs: a list of player models
    Creates or updates a player week based on the current player and the date. 
    If there is an already existing player week for the current date period, 
    it updates. Otherwise, create a new one.
    """
    deta = Deta(project_key)
    db = deta.Base(db_prefix+'rating_weeks')
    # hit the chess.com api and then the lichess api
    # scrape the fide website for ratings or maybe chess.com/players
    # eventually go for finding fide games
    # then make a new rating_day
    # also scrape from the youtube api and from a twitch api to get that data
    for player in players:
        # first get the required fide ratings to initialized a
        r = requests.get(
            f'https://ratings.fide.com/profile/{player.fide_id}').text
        soup = BeautifulSoup(r)
        classical_rating = int(
            soup.find(class_='profile-top-rating-data_gray').text[3:])  # std 2669
        rapid_rating = int(
            soup.find(class_='profile-top-rating-data_red').text[6:])  # rapid 2669
        blitz_rating = int(
            soup.find(class_='profile-top-rating-data_blue').text[6:])  # blitz 2669
        # next check if there is a week in progress
        week = db.fetch(
            [{"end_day?gte": datetime.date.today()}, {"player": player}]).items
        # if there is not a week in progress, create one
        if len(week) == 0:
            previous_weeks = db.fetch({"player": player}).items
            if len(previous_weeks) == 0:
                today = datetime.date.today()
                # all weeks start on Mondays
                start_day = today + \
                    datetime.timedelta(days=-today.weekday(), weeks=1)
                week = db.put(Rating_week(
                    player=player,
                    week_number=0,  # weeks start at 0
                    start_day=start_day,
                    end_day=start_day + datetime.timedelta(days=7),
                    fide_classical=classical_rating,
                    fide_rapid=rapid_rating,
                    fide_blitz=blitz_rating,
                ))
            else:
                previous_week = sorted(
                    previous_weeks, key=lambda x: x.week_number, reverse=True)[0]
                week = db.put(Rating_week(
                    player=player,
                    week_number=previous_week.week_number + 1,
                    start_day=previous_week.start_day +
                    datetime.timedelta(days=7),
                    end_day=previous_week.end_day + datetime.timedelta(days=7),
                    fide_classical=classical_rating,
                    fide_rapid=rapid_rating,
                    fide_blitz=blitz_rating,
                ))
        else:
            week = week[0]
        # requests to lichess, chess, twitch, and youtube
        if not isinstance(player.lichess_username, type(None)):
            r = requests.get()


@app.lib.cron()
def cron_job(event):
    deta = Deta(project_key)
    db = deta.Base(db_prefix+'players')
    players = db.fetch().items
    create_update_rating_week(players)
    return f"Rating weeks created or updated for {len(players)} players"


router = APIRouter()


@app.get("/")
async def read_root():
    return {"The API for": "Fantasy Chess League!!!", "Visit /docs": "to see the API documentation"}
