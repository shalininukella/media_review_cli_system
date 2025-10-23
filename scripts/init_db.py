import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import init_db, get_session
from app.models import User, Media


def seed_data():
    session = get_session()

    # Delete all rows
    session.query(Media).delete()

    if session.query(User).count() == 0:
        users = [User(name="Alice"), User(name="Bob"), User(name="Charlie")]
        session.add_all(users)

    if session.query(Media).count() == 0:
        media_list = [
            Media(title="Inception", type="movie"),
            Media(title="Stranger Things", type="show"),
            Media(title="Shape of You", type="song"),
        ]
        session.add_all(media_list)

    session.commit()
    print("Seed data added.")


if __name__ == "__main__":
    init_db()
    print("Database initialized at: ", Path("data/media_review.db").resolve())
    seed_data()
