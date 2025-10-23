from app.models import Movie, Show, Song

class MediaFactory:
    @staticmethod
    def create_media(title, media_type):
        if media_type == "movie":
            return Movie(title = title)
        elif media_type == "show":
            return Show(title = title)
        elif media_type == "song":
            return Song(title = title)
        else:
            raise ValueError(f"unknown media type : {media_type}")
