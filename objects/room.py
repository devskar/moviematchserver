from objects.user import User


class Room:
    def __init__(self, id, mm, name):

        self.mm = mm

        self.name = name
        self.id = id
        self.admin = None

        self.participants = set()

        self.current_movie = mm.get_random_movie()

        self.positive_votes = set()
        self.negative_votes = set()

    def positive_vote_movie(self, user):
        self.positive_votes.add(user)

    def negative_vote_movie(self, user):
        self.negative_votes.add(user)

    def reset_votes(self):
        self.positive_votes.clear()
        self.negative_votes.clear()

    def everyone_voted(self):
        return self.get_vote_count() == len(self.participants)

    def get_vote_count(self):
        return len(self.positive_votes.union(self.negative_votes))

    def add_user(self, user: User):
        """Adds a user to the room. first one will be the admin of the room"""
        if len(self.participants) == 0:
            self.admin = user

        self.participants.add(user)

    def remove_user(self, user):
        """Remove a user from the room"""

        if user in self.participants:

            self.participants.remove(user)

            if user in self.negative_votes:
                self.negative_votes.remove(user)
            if user in self.positive_votes:
                self.positive_votes.remove(user)

    def is_closed(self):
        # if no users are in the room the room closes
        if len(self.participants) == 0:
            return True
        return False
