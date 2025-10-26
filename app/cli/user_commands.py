from app.services import user_service

def add_user(name):
    result = user_service.add_user(name)
    print(result["message"])


def list_users():
    result = user_service.list_users()

    if not result["success"]:
        print(result["message"])
        return

    users = result["data"]
    if not users:
        print("No users found.")
        return

    print("Users:")
    for u in users:
        print(f"  - [{u['id']}] {u['name']}")

