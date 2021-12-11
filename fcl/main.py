from fastapi import FastAPI, APIRouter, HTTPException, status
from deta import Deta, App
from models import *
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


router = APIRouter()


@app.get("/")
async def read_root():
    return {"The API for": "Fantasy Chess League!!!", "Visit /docs": "to see the API documentation"}
