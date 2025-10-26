from app.services import review_service

def add_review_command(media_id, rating, comment):
    try:
        user_id = int(input("Enter the user ID: "))
    except ValueError:
        print("Invalid user ID.")
        return

    result = review_service.add_review(user_id, media_id, rating, comment)
    print(result["message"])


def list_reviews_command():
    result = review_service.list_reviews()

    if not result["success"]:
        print(result["message"])
        return

    reviews = result["data"]
    if not reviews:
        print("No reviews yet.")
        return

    for r in reviews:
        print(f"[{r['id']}] {r['user_id']} ({r['media_title']}), {r['rating']}, {r['comment']}")

