from fastapi import FastAPI, HTTPException
from datetime import date, datetime, timedelta
import random
from DTO import Game, News, Community, User, UserCreate, UserLogin



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

# 가상의 사용자 데이터베이스
fake_users_db = []
# 가상의 게임 데이터
_sample_games = [
    {
        "id": 1,
        "name": "Stardew Valley",
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
        "views": 0,
        "likes": 0,
        "purchase_link": "https://store.steampowered.com/app/413150/Stardew_Valley/",
        "image_path": [
            "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg?t=1666917466",
            "https://cdn.akamai.steamstatic.com/steam/apps/413150/ss_d836f0a5b0447fb6a2bdb0a6ac5f954949d3c41e.116x65.jpg?t=1666917466"
        ],
        "video_path": ["https://youtu.be/ot7uXNQskhs"]
    },
    {
        "id": 2,
        "name": "Example Game 2",
        "description": "This is an example game description.",
        "price": 2500,
        "release_date": "2022-10-15",
        "developer": "Game Studio XYZ",
        "publisher": "Publisher ABC",
        "genre": ["Action", "Adventure"],
        "tags": ["Shooter", "Exploration", "Sci-Fi"],
        "game_rating": ["Teen", "Violence"],
        "game_censorship": ["Violence", "Strong Language"],
        "platform": ["Windows", "PlayStation", "Xbox", "Nintendo Switch"],
        "game_requirements": [
            {"OS": "Windows 10", "Processor": "Quad-core", "Memory": "8 GB RAM", "Graphics": "NVIDIA GTX 1060", "Storage": "20 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/game2/",
        "image_path": [
            "https://example.com/game2/images/1.jpg"
        ],
        "video_path": ["https://example.com/game2/videos/trailer.mp4"]
    },
    {
        "id": 3,
        "name": "Fantasy Quest",
        "description": "Embark on a journey through a magical realm...",
        "price": 2999,
        "release_date": "2023-04-05",
        "developer": "Mythical Games",
        "publisher": "Adventure Studios",
        "genre": ["RPG", "Fantasy"],
        "tags": ["Questing", "Magic", "Medieval", "Exploration"],
        "game_rating": ["10+", "Fantasy Violence"],
        "game_censorship": [],
        "platform": ["Windows", "macOS", "Nintendo Switch"],
        "game_requirements": [
            {"OS": "Windows 7", "Processor": "Dual-core", "Memory": "4 GB RAM", "Graphics": "Intel HD Graphics", "Storage": "10 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/fantasyquest/",
        "image_path": [
            "https://example.com/fantasyquest/images/cover.jpg",
            "https://example.com/fantasyquest/images/screenshots/1.jpg",
            "https://example.com/fantasyquest/images/screenshots/2.jpg"
        ],
        "video_path": []
    },
    {
        "id": 4,
        "name": "Space Odyssey",
        "description": "Explore the universe in this epic space adventure...",
        "price": 3499,
        "release_date": "2023-07-20",
        "developer": "Galactic Studios",
        "publisher": "Cosmic Games",
        "genre": ["Simulation", "Adventure"],
        "tags": ["Space Exploration", "Sci-Fi", "Aliens"],
        "game_rating": ["12+", "Fantasy Violence"],
        "game_censorship": [],
        "platform": ["Windows", "macOS"],
        "game_requirements": [
            {"OS": "Windows 8", "Processor": "Quad-core", "Memory": "6 GB RAM", "Graphics": "NVIDIA GTX 1650", "Storage": "15 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/spaceodyssey/",
        "image_path": [
            "https://example.com/spaceodyssey/images/cover.jpg",
            "https://example.com/spaceodyssey/images/screenshots/1.jpg",
            "https://example.com/spaceodyssey/images/screenshots/2.jpg"
        ],
        "video_path": []
    },
    {
        "id": 5,
        "name": "Mystic Spells",
        "description": "Unleash the power of magic in this enchanting adventure...",
        "price": 1999,
        "release_date": "2023-06-10",
        "developer": "Spellbound Studios",
        "publisher": "Magic Games Inc.",
        "genre": ["Adventure", "Fantasy"],
        "tags": ["Magic Spells", "Questing", "Wizards"],
        "game_rating": ["10+", "Fantasy Violence"],
        "game_censorship": [],
        "platform": ["Windows"],
        "game_requirements": [
            {"OS": "Windows 7", "Processor": "Dual-core", "Memory": "4 GB RAM", "Graphics": "Intel HD Graphics", "Storage": "8 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/mysticspells/",
        "image_path": [
            "https://example.com/mysticspells/images/cover.jpg",
            "https://example.com/mysticspells/images/screenshots/1.jpg",
            "https://example.com/mysticspells/images/screenshots/2.jpg"
        ],
        "video_path": []
    },
    {
        "id": 6,
        "name": "Racing Rivals",
        "description": "Rev up your engines and compete in high-speed races...",
        "price": 2999,
        "release_date": "2023-03-15",
        "developer": "Velocity Studios",
        "publisher": "Race Games Ltd.",
        "genre": ["Racing", "Sports"],
        "tags": ["High-Speed", "Multiplayer", "Tracks"],
        "game_rating": ["E for Everyone"],
        "game_censorship": [],
        "platform": ["Windows", "PlayStation", "Xbox"],
        "game_requirements": [
            {"OS": "Windows 10", "Processor": "Quad-core", "Memory": "8 GB RAM", "Graphics": "NVIDIA GTX 1060", "Storage": "25 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/racingrivals/",
        "image_path": [
            "https://example.com/racingrivals/images/cover.jpg",
            "https://example.com/racingrivals/images/screenshots/1.jpg",
            "https://example.com/racingrivals/images/screenshots/2.jpg"
        ],
        "video_path": ["https://example.com/racingrivals/videos/trailer.mp4"]
    },
    {
        "id": 7,
        "name": "Ancient Quest",
        "description": "Embark on a historical journey to uncover ancient mysteries...",
        "price": 2499,
        "release_date": "2023-01-05",
        "developer": "Historical Games",
        "publisher": "Archaeo Studios",
        "genre": ["Adventure", "Historical"],
        "tags": ["Exploration", "Artifacts", "Archaeology"],
        "game_rating": ["Teen", "Mild Violence"],
        "game_censorship": [],
        "platform": ["Windows", "macOS"],
        "game_requirements": [
            {"OS": "Windows 8", "Processor": "Dual-core", "Memory": "4 GB RAM", "Graphics": "Intel HD Graphics", "Storage": "12 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/ancientquest/",
        "image_path": [
            "https://example.com/ancientquest/images/cover.jpg",
            "https://example.com/ancientquest/images/screenshots/1.jpg",
            "https://example.com/ancientquest/images/screenshots/2.jpg"
        ],
        "video_path": []
    },
    {
        "id": 8,
        "name": "Survival Island",
        "description": "Stranded on a deserted island, you must fight to survive...",
        "price": 1999,
        "release_date": "2022-09-10",
        "developer": "Survive Studios",
        "publisher": "Island Games Inc.",
        "genre": ["Survival", "Adventure"],
        "tags": ["Crafting", "Exploration", "Wildlife"],
        "game_rating": ["Teen", "Violence"],
        "game_censorship": ["Violence"],
        "platform": ["Windows", "macOS"],
        "game_requirements": [
            {"OS": "Windows 7", "Processor": "Dual-core", "Memory": "4 GB RAM", "Graphics": "Intel HD Graphics", "Storage": "10 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/survivalisland/",
        "image_path": [
            "https://example.com/survivalisland/images/cover.jpg",
            "https://example.com/survivalisland/images/screenshots/1.jpg",
            "https://example.com/survivalisland/images/screenshots/2.jpg"
        ],
        "video_path": []
    },
    {
        "id": 9,
        "name": "Mystic Spells",
        "description": "Unleash the power of magic in this enchanting adventure...",
        "price": 1999,
        "release_date": "2023-06-10",
        "developer": "Spellbound Studios",
        "publisher": "Magic Games Inc.",
        "genre": ["Adventure", "Fantasy"],
        "tags": ["Magic Spells", "Questing", "Wizards"],
        "game_rating": ["10+", "Fantasy Violence"],
        "game_censorship": [],
        "platform": ["Windows"],
        "game_requirements": [
            {"OS": "Windows 7", "Processor": "Dual-core", "Memory": "4 GB RAM", "Graphics": "Intel HD Graphics", "Storage": "8 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/mysticspells/",
        "image_path": [
            "https://example.com/mysticspells/images/cover.jpg",
            "https://example.com/mysticspells/images/screenshots/1.jpg",
            "https://example.com/mysticspells/images/screenshots/2.jpg"
        ],
        "video_path": []
    },
    {
        "id": 10,
        "name": "City Builder",
        "description": "Build and manage your own city in this urban simulation game...",
        "price": 2999,
        "release_date": "2023-04-22",
        "developer": "Urban Creations",
        "publisher": "City Games Ltd.",
        "genre": ["Simulation", "Strategy"],
        "tags": ["City Management", "Urban Planning", "Economy"],
        "game_rating": ["E for Everyone"],
        "game_censorship": [],
        "platform": ["Windows", "macOS"],
        "game_requirements": [
            {"OS": "Windows 10", "Processor": "Quad-core", "Memory": "8 GB RAM", "Graphics": "NVIDIA GTX 1060", "Storage": "15 GB available space"}
        ],
        "views": 0,
        "likes": 0,
        "purchase_link": "https://example.com/citybuilder/",
        "image_path": [
            "https://example.com/citybuilder/images/cover.jpg",
            "https://example.com/citybuilder/images/screenshots/1.jpg",
            "https://example.com/citybuilder/images/screenshots/2.jpg"
        ],
        "video_path": ["https://example.com/citybuilder/videos/trailer.mp4"]
    }
]
# 가상의 뉴스 데이터
_sample_news = [
    {
        "id": 1,
        "title": "Exciting New Feature Release!",
        "content": "We are thrilled to announce the launch of our latest feature...",
        "author": "John Doe",
        "written_date": "2023-08-17T09:00:00",
        "last_modified_date": "2023-08-17T14:30:00",
        "views": 1500,
        "likes": 62,
        "image_path": [
            "https://example.com/news/images/1.jpg",
            "https://example.com/news/images/2.jpg"
        ],
        "video_path": [
            "https://example.com/news/videos/1.mp4"
        ]
    },
    {
        "id": 2,
        "title": "Upcoming Event Announcement",
        "content": "Get ready for an unforgettable event happening next week...",
        "author": "Jane Smith",
        "written_date": "2023-08-16T11:30:00",
        "last_modified_date": "2023-08-16T15:45:00",
        "views": 1200,
        "likes": 42,
        "image_path": [
            "https://example.com/news/images/3.jpg"
        ],
        "video_path": []
    },
    {
        "id": 3,
        "title": "Industry Award Recognition",
        "content": "We are honored to receive the prestigious Industry Award...",
        "author": "Alex Johnson",
        "written_date": "2023-08-15T14:15:00",
        "last_modified_date": "2023-08-15T14:15:00",
        "views": 2200,
        "likes": 93,
        "image_path": [
            "https://example.com/news/images/4.jpg",
            "https://example.com/news/images/5.jpg"
        ],
        "video_path": []
    },
    {
        "id": 4,
        "title": "Product Update and Enhancements",
        "content": "Check out the latest enhancements we've made to our product...",
        "author": "Emily Brown",
        "written_date": "2023-08-14T08:45:00",
        "last_modified_date": "2023-08-14T08:45:00",
        "views": 1800,
        "likes": 75,
        "image_path": [],
        "video_path": []
    },
    {
        "id": 5,
        "title": "Exclusive Interview with Industry Expert",
        "content": "We sat down with the leading expert in the industry to discuss...",
        "author": "Michael Lee",
        "written_date": "2023-08-13T17:30:00",
        "last_modified_date": "2023-08-13T17:30:00",
        "views": 2800,
        "likes": 112,
        "image_path": [
            "https://example.com/news/images/6.jpg"
        ],
        "video_path": [
            "https://example.com/news/videos/2.mp4"
        ]
    },
    {
        "id": 6,
        "title": "Company Milestone Celebration",
        "content": "We're excited to commemorate our company's significant milestone...",
        "author": "David Wilson",
        "written_date": "2023-08-12T10:20:00",
        "last_modified_date": "2023-08-12T10:20:00",
        "views": 1900,
        "likes": 88,
        "image_path": [
            "https://example.com/news/images/7.jpg",
            "https://example.com/news/images/8.jpg"
        ],
        "video_path": []
    },
    {
        "id": 7,
        "title": "Product Launch Event Recap",
        "content": "Catch a glimpse of the exciting moments from our recent product launch...",
        "author": "Sarah Johnson",
        "written_date": "2023-08-11T13:10:00",
        "last_modified_date": "2023-08-11T13:10:00",
        "views": 3200,
        "likes": 132,
        "image_path": [
            "https://example.com/news/images/9.jpg"
        ],
        "video_path": [
            "https://example.com/news/videos/3.mp4"
        ]
    },
    {
        "id": 8,
        "title": "Customer Testimonials",
        "content": "Read what our satisfied customers are saying about their experiences...",
        "author": "Lisa Martinez",
        "written_date": "2023-08-10T15:45:00",
        "last_modified_date": "2023-08-10T15:45:00",
        "views": 2500,
        "likes": 103,
        "image_path": [],
        "video_path": []
    },
    {
        "id": 9,
        "title": "Industry Trends Report",
        "content": "Explore the latest trends and insights in the industry with our comprehensive report...",
        "author": "Daniel Kim",
        "written_date": "2023-08-09T09:30:00",
        "last_modified_date": "2023-08-09T09:30:00",
        "views": 3100,
        "likes": 120,
        "image_path": [
            "https://example.com/news/images/10.jpg"
        ],
        "video_path": []
    },
    {
        "id": 10,
        "title": "New Partnership Announcement",
        "content": "We are excited to announce our strategic partnership with...",
        "author": "Jessica Liu",
        "written_date": "2023-08-08T11:20:00",
        "last_modified_date": "2023-08-08T11:20:00",
        "views": 2700,
        "likes": 98,
        "image_path": [
            "https://example.com/news/images/11.jpg"
        ],
        "video_path": []
    }
]

## --Sample Data



## 이메일 함수--

import smtplib
from email.message import EmailMessage

# 이메일 인증코드 생성 함수
def generate_verification_code():
    return str(random.randint(100000, 999999))

# 사용자의 이메일과 해당 인증코드, 생성 시간을 저장하는 딕셔너리
email_verification_codes = {}

# 이메일 발송 함수
def send_verification_email(email, code):
    subject = "Email Verification Code"
    message = f"Your verification code is: {code}"
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = "barleymilk640@gmail.com"  # 발송 이메일 주소
    msg["To"] = email

    # Gmail 사용 예시
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("barleymilk640@gmail.com", "gtzzwqhxpfdavmje")  # 발송 이메일 계정 정보
    server.send_message(msg)
    server.quit()

## --이메일 함수



app = FastAPI()

## 메인페이지
@app.get("/")
async def root():
    game_data = _sample_games[:6]  # 첫 6개의 게임 데이터 가져오기
    news_data = _sample_news[:6]    # 첫 6개의 뉴스 데이터 가져오기

    games = [Game(**game) for game in game_data]
    news = [News(**news) for news in news_data]

    return {"games": games, "news": news}

## 회원가입
@app.post("/register")
async def register(user: UserCreate):
    verification_code = generate_verification_code()
    send_verification_email(user.email, verification_code)

    new_user = User(
        id=len(fake_users_db) + 1,
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        nickname=user.nickname,
        birth_date=user.birth_date,
        profile_image=user.profile_image,
        created_at=datetime.now(),
        access_token="your_generated_access_token",
        reports=0
    )
    fake_users_db.append(new_user)

    # 이메일 인증코드 저장 : 인증코드, 생성시간, 만료시간(5분 설정)
    email_verification_codes[user.email] = {
        "code": verification_code,
        "creation_time": datetime.now(),
        "expiration_time": datetime.now() + timedelta(minutes=5)
    }

    return {"message": "User registered successfully"}

## 회원가입 > 이메일 검증
@app.post("/verify")
async def verify_email(email: str, code: str):
    if email in email_verification_codes:
        current_time = datetime.now()
        if current_time <= email_verification_codes[email]["expiration_time"]:
            if code == email_verification_codes[email]["code"]:
                return {"message": "Email verified successfully"}
    
    raise HTTPException(status_code=400, detail="Email verification failed")

## 로그인
@app.post("/login")
async def login(user_login: UserLogin):
    user = next((u for u in fake_users_db if u.email == user_login.email), None)
    if user is None or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user.access_token}

## 뉴스페이지
@app.get("/news")
async def news():
    news = [News(**news_data) for news_data in _sample_news]
    return news

@app.get("/games")
async def games():
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