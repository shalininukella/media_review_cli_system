from app.services import recommendation_service

def get_top_rated_command(limit=5):
    result = recommendation_service.get_top_rated(limit)
    if not result["success"]:
        print(result["message"])
        return

    print("Top Rated Media:")
    for title, avg in result["data"]:
        print(f" - {title}: {avg:.1f}")


def recommend_media_command(user_id, limit=5):
    result = recommendation_service.recommend_media(user_id, limit)

    if not result["success"]:
        print(result["message"])
        return

    user_name = result["user_name"]
    recommendations = result["data"]

    print(f"Recommendations for {user_name}:")
    if recommendations:
        for title, avg in recommendations:
            print(f" - {title} (avg rating: {avg:.1f})")
    else:
        print("No recommendations available.")
