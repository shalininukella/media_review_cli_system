from app.db import get_session
from app.models import User


def add_user(name):
    session = get_session()

    existing_user = session.query(User).filter_by(name=name).first()
    if existing_user:
        print(f"User '{name}' already exists.")
        return existing_user

    user = User(name=name)
    session.add(user)
    session.commit()

    print(f"Added user '{name}' successfully.")
    return user


def list_users():
    session = get_session()

    users = session.query(User).all()
    if not users:
        print("No users found.")
        return

    print("Users:")
    for u in users:
        print(f"  - [{u.id}] {u.name}")
