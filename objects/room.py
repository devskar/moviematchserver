from objects.user import User
from manager.moviemanager import Genre, Language


class Room:
    def __init__(self, id, movie_manager):

        self.movie_manager = movie_manager

        self.id = id
        self.admin = None

        self.participants = set()

        self.genre = Genre.ALL
        self.language = Language.EN

        self.current_movie = None

    def change_genre(self, genre):
        """Changes the current genre of the room"""
        self.genre = genre

    def add_user(self, user: User):
        """Adds a user to the room. first one will be the admin of the room"""
        if len(self.participants) == 0:
            self.admin = user

        self.participants.add(user)

    def remove_user(self, user):
        """Remove a user from the room"""
        self.participants.remove(user)


