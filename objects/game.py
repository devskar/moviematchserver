from objects.room import Room
from objects.user import User
from manager.moviemanager import MovieManager


class Game:

    def __init__(self):
        self.current_user = set()
        self.current_rooms = set()

        self.latest_room_id = 1

        self.movie_manager = MovieManager()

    def register_user(self, sid, name):
        """Initialize a new user"""

        user = User(sid, name)
        self.current_user.add(user)

        return user

    def find_user_by_sid(self, user_sid):
        """Find a user by its id"""

        for user in self.current_user:
            if user.sid == user_sid:
                return user

    def create_room(self, name):
        """Create a room and adds the creator to it"""
        room = Room(self.latest_room_id, self.movie_manager, name)

        self.current_rooms.add(room)

        self.latest_room_id += 1

        return room

    def join_room(self, user, room_id):
        """Add a user to a room"""

        room = self.find_room_by_id(room_id)

        if room:
            room.add_user(user)

    def find_room_by_id(self, room_id):
        """Find a room by its id"""

        for room in self.current_rooms:
            if room.id == room_id:
                return room

    def find_room_by_user(self, user_sid):
        """Find a room by the sid of a user"""

        for room in self.current_rooms:
            for user in room.participants:
                if user.sid == user_sid:
                    return room

