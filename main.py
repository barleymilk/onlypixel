from fastapi import FastAPI
from DTO import Game, News, Community

## DEBUG--
import logging
import sys

mylogger = logging.getLogger("mylogger")

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

mylogger.addHandler(handler)
mylogger.setLevel(logging.DEBUG)
## --DEBUG

## Sample Data--
_sample_games = [
    {
        "id":1, 
        "name":"Stardew Valley", 
        "description": "You've inherited your grandfather's old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life. Can you learn to live off the land and turn these overgrown fields into a thriving home?",
        "price": 16000,
        "release_date": "2016-02-27",
        "developer": "ConcernedApe",
        "publisher": "ConcernedApe",
        "genre": ["Indie", "RPG", "Simulation"],
        "tags": ["Farming Sim", "Life Sim", "Pixel Graphics", "Multiplayer", "RPG", "Relaxing", "Agriculture", "Simulation", "Crafting", "Sandbox", "Indie", "Building", "Singleplayer", "Casual", "Open World", "2D", "Cute", "Great Soundtrack", "Dating Sim", "Fishing"],
        "game_rating": ["12세 이용가", "모바일: 15세 이용가"],
        "game_censorship": ["마약", "주류", "담배"],
        "platform": ["Windows", "macOS", "SteamOS+Linux", "AOS", "IOS"],
        "game_requirements": [
            {"OS": "Windows Vista or greater", "Processor": "2 Ghz", "Memory": "2 GB RAM", "Graphics": "256 mb video memory, shader model 3.0+", "DirectX": "Version 10", "Storage": "500 MB available space"},
            {"OS": "Mac OSX 10.10+", "Processor": "2 Ghz", "Memory": "2 GB RAM", "Graphics": "256 mb video memory, OpenGL 2", "Storage": "500 MB available space"},
            {"OS": "Ubuntu 12.04 LTS", "Processor": "2 Ghz", "Memory": "2 GB RAM", "Graphics": "256 mb video memory, OpenGL 2", "Storage": "500 MB available space"}
        ],
        "purchase_link": "https://store.steampowered.com/app/413150/Stardew_Valley/",
        "image_path": [
            "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg?t=1666917466",
            "https://cdn.akamai.steamstatic.com/steam/apps/413150/ss_d836f0a5b0447fb6a2bdb0a6ac5f954949d3c41e.116x65.jpg?t=1666917466"
        ],
        "video_path": ["https://youtu.be/ot7uXNQskhs"]
    },
    {
        "id":2, 
        "name":"Stardew Valley", 
        "description": "You've inherited your grandfather's old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life. Can you learn to live off the land and turn these overgrown fields into a thriving home?",
        "price": 16000,
        "release_date": "2016-02-27",
        "developer": "ConcernedApe",
        "publisher": "ConcernedApe",
        "genre": ["Indie", "RPG", "Simulation"],
        "tags": ["Farming Sim", "Life Sim", "Pixel Graphics", "Multiplayer", "RPG", "Relaxing", "Agriculture", "Simulation", "Crafting", "Sandbox", "Indie", "Building", "Singleplayer", "Casual", "Open World", "2D", "Cute", "Great Soundtrack", "Dating Sim", "Fishing"],
        "game_rating": ["12세 이용가", "모바일: 15세 이용가"],
        "game_censorship": ["마약", "주류", "담배"],
        "platform": ["Windows", "macOS", "SteamOS+Linux", "AOS", "IOS"],
        "game_requirements": [
            {"OS": "Windows Vista or greater", "Processor": "2 Ghz", "Memory": "2 GB RAM", "Graphics": "256 mb video memory, shader model 3.0+", "DirectX": "Version 10", "Storage": "500 MB available space"},
            {"OS": "Mac OSX 10.10+", "Processor": "2 Ghz", "Memory": "2 GB RAM", "Graphics": "256 mb video memory, OpenGL 2", "Storage": "500 MB available space"},
            {"OS": "Ubuntu 12.04 LTS", "Processor": "2 Ghz", "Memory": "2 GB RAM", "Graphics": "256 mb video memory, OpenGL 2", "Storage": "500 MB available space"}
        ],
        "purchase_link": "https://store.steampowered.com/app/413150/Stardew_Valley/",
        "image_path": [
            "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg?t=1666917466",
            "https://cdn.akamai.steamstatic.com/steam/apps/413150/ss_d836f0a5b0447fb6a2bdb0a6ac5f954949d3c41e.116x65.jpg?t=1666917466"
        ],
        "video_path": ["https://youtu.be/ot7uXNQskhs"]
    }
]
## --Sample Data

app = FastAPI()

@app.get("/")
async def root():
    games = [Game(**game_data) for game_data in _sample_games]
    return games

@app.get("/games/{game_id}")
async def games(game_id: int):
    game = None
    for _game_data in _sample_games:
        if _game_data['id'] == game_id:
            game = Game(**_game_data)
    return game

@app.post("/posts")
def create_post(post: Community):
    mylogger.debug(post)
    return None

# uvicorn main:app --reload