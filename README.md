# 🎬 Media Review CLI

A command-line application to review Movies, Web Shows, and Songs.

## 📁 Project Structure
```bash
media_review/
├── app/
│ ├── init.py
│ ├── db.py # SQLAlchemy DB setup
│ ├── models.py # User, Media, Reviews models
│ ├── media_factory.py # Factory pattern for media creation
│ ├── observer/ # Observer pattern (notifications)
│ ├── cli/ # CLI commands (media, reviews)
│ └── cache.py # Redis cache setup
│
├── scripts/
│ └── init_db.py # Initialize & seed database
│
├── data/
│ └── media_review.db # SQLite database (auto-created)
│
├── media_review.py # CLI launcher (entrypoint)
├── docker-compose.yml # Redis container setup
├── requirements.txt
├──Dockerfile
└── README.md


---

## 🧰 Requirements

- Python 3.10+
- Docker Desktop (for Redis container)
- Virtual environment (`venv`)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone & Navigate
```bash
cd C:\Users\NukellaShalini\media_review

### 2️⃣ Create and Activate Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate

###3️⃣ Install Dependencies
pip install -r requirements.txt

###4️⃣ Start Redis (via Docker)

###Run only Redis container — app runs locally.

docker compose up -d


### Check container status:

docker ps


You should see something like media_review_redis.

###5️⃣ Initialize Database (first time only)
python -m scripts.init_db


This creates data/media_review.db and seeds sample data.

### 🚀 Run the App

Use the following CLI commands:

Command	Description
python media_review.py --list	List all media
python media_review.py --review <media_id> <rating> <comment>	Add a review
python media_review.py --search "<title>"	Search media + show cached reviews
python media_review.py --top-rated	Show top-rated media
python media_review.py --recommend <user_id> Show the recommendations

###🧠 Features

✅ Factory Pattern — Dynamically creates Movie, Song, etc.
✅ Observer Pattern — Notifies users who favorited a media when new reviews appear.
✅ Redis Caching — Caches frequently accessed reviews for faster retrieval.
✅ Multithreading (optional) — Supports concurrent review submissions.
✅ Dockerized Redis — Keeps caching isolated and easily manageable.

###🧹 Shut Down Redis

### When you’re done:

docker compose down


### If you also want to delete Redis data:

docker compose down -v

### 🧩 Notes

Database: SQLite (stored at data/media_review.db)

Cache: Redis (port 6379)

Redis cache TTL: 120 seconds

Code entrypoint: media_review.py

💡 Example Run
# List media
python media_review.py --list

# Add a review
python media_review.py --review 1 5 "Amazing movie!"

# Search for reviews (cached)
python media_review.py --search "Inception"

# Get top-rated media
python media_review.py --top-rated

###🐳 Optional: Auto-start Helper

You can create a small batch file (start_all.bat) for convenience:

@echo off
cd C:\Users\NukellaShalini\media_review
call .venv\Scripts\activate
docker compose up -d
echo.
echo Project environment started. Run commands like:
echo python media_review.py --list
pause


Author: Nukella Shalini
License: MIT