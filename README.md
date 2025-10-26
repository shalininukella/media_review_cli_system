# 🎬 Media Review CLI

A modular **command-line application** to manage and review **Movies, Web Shows, and Songs**, with Redis caching, Observer notifications, and concurrent review support.

---

## 📁 Project Structure

```bash
media_review/
├── app/
│   ├── core/
│   │   ├── db.py               # SQLAlchemy database setup
│   │   └── models.py           # ORM models: User, Media, Reviews, Favourites
│   │
│   ├── services/
│   │   ├── recommendation_service.py  # Top-rated & personalized recommendations
│   │   ├── favourite_service.py       # Manage user favourites
│   │   ├── review_service.py          # Review creation & listing logic
│   │   ├── concurrency_service.py     # Handles concurrent (threaded) reviews
│   │   └── user_service.py    # listing and adding users
│   │   ├── media_service.py  # Top-rated & personalized recommendations
│   │
│   ├── observer/                 # Observer pattern for notifications
│   │   ├── __init__.py
│   │   ├── base.py               # Observer & Subject base classes
│   │   ├── observer_manager.py   # ReviewNotifier, attachment logic
│   │   └── notifications_service.py  # Concrete notification services
│   │
│   ├── cli/
│   │   ├── main.py             # CLI command parser (entry for all CLI actions)
│   │   ├── user_commands.py    # CLI commands for users
│   │   ├── media_commands.py   # CLI commands for media
│   │   ├── review_commands.py  # CLI commands for reviews
│   │   ├── favourite_commands.py  # CLI commands for favourites
│   │   ├── recommendation_commands.py  # CLI commands for recommendations
│   │   └── concurrency.py      # CLI wrapper for concurrent review simulation
│   │
│   ├── utils.py                # Common helper functions
│   ├── cache.py                # Redis cache setup
│   ├── logging_config.py       # Logging setup for app-wide logging
│   └── media_factory.py        # Factory pattern for dynamic media creation
│
├── scripts/
│   ├── init_db.py              # Initialize empty database
│   └── seed_dev_data.py        # Seed database with development data
│
├── data/
│   └── media_review.db         # SQLite database (auto-created)
│
├── logs/
│   └── app.log                 # Auto-generated log file
│
├── media_review.py             # Main CLI launcher
├── docker-compose.yml          # Redis container setup
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🧰 Requirements

* **Python 3.10+**
* **Docker Desktop** (for Redis)
* **Virtual environment (`venv`)**

---

## ⚙️ Setup Instructions

### 1️⃣ Clone & Navigate

```bash
git clone <repo_url>
cd media_review
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start Redis (via Docker)

```bash
docker compose up -d
```

Verify container:

```bash
docker ps
```

You should see a container like `media_review_redis`.

### 5️⃣ Initialize or Seed the Database

```bash
python -m scripts.init_db
# or
python -m scripts.seed_dev_data
```

This creates a new SQLite DB at `data/media_review.db` with sample data.

---

## 🚀 Run the App

All commands are executed via:

```bash
python media_review.py <command>
```

### CLI Commands

| ------------------------------------------------------ | -------------------------------- |
| Command                                                | Description                      |
| ------------------------------------------------------ | -------------------------------- |
| `--list`                                               | List all media                   |
| `--add-media <title> <type>`                           | Add new media (movie/show/song)  |
| `--search "<title>"`                                   | Search media by title            |
| `--review <media_id> <rating> <comment>`               | Add a review                     |
| `--show-reviews`                                       | Display all reviews              |
| `--top-rated`                                          | Show top-rated media             |
| `--recommend <user_id>`                                | Recommend media for a user       |
| `--favourite <media_id> <user_id>`                     | Add to favourites                |
| `--unfavourite <media_id> <user_id>`                   | Remove from favourites           |
| `--show-favourites <user_id>`                          | Show a user’s favourites         |
| `--concurrent <user_id> <media_id> <rating> <comment>` | Simulate concurrent user reviews |
| `--add-user <name>`                                    | Add a user                       |
| `--list-users`                                         | List all users                   |
| ------------------------------------------------------ | -------------------------------- |

---

## 🧠 Features

✅ **Factory Pattern** – Creates `Movie`, `Show`, and `Song` dynamically.
✅ **Observer Pattern** – Notifies users when new reviews appear for their favourites.
✅ **Service Layer** – Business logic separated from CLI and database.
✅ **Redis Caching** – Fast retrieval of frequently accessed media data.
✅ **Logging System** – All actions logged in `logs/app.log`.
✅ **ThreadPoolExecutor** – Handles concurrent reviews safely.
✅ **Dockerized Redis** – Clean caching setup isolated via container.

---

## 🧹 Shut Down Redis

When you’re done:

```bash
docker compose down
```

To also remove cached Redis data:

```bash
docker compose down -v
```

---

## 🧩 Notes

* **Database:** `SQLite` at `data/media_review.db`
* **Cache:** Redis (port `6379`)
* **Cache TTL:** 300 seconds (5 minutes)
* **Entry Point:** `media_review.py`

---

## 💡 Example Usage

```bash
# List media
python media_review.py --list

# Add a new user
python media_review.py --add-user "Alice"

# Add a media
python media_review.py --add-media "Inception" movie

# Add a review
python media_review.py --review 1 4.5 "Amazing movie!"

# Search media (cached)
python media_review.py --search "Inception"

# Get recommendations
python media_review.py --recommend 1

# Show favourites
python media_review.py --show-favourites 1
```

---

## 🧩 Optional: Quick Start Batch (Windows)

Create a file `start_all.bat`:

```bat
@echo off
cd C:\Users\NukellaShalini\media_review
call .venv\Scripts\activate
docker compose up -d
echo.
echo Project started! Try:
echo python media_review.py --list
pause
```

---

**Author:** Nukella Shalini
**License:** MIT
