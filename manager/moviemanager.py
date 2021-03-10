from enum import Enum
import requests
import random
import pprint

API_URL = 'https://api.themoviedb.org/3/'
POSTER_URL = 'https://image.tmdb.org/t/p/w500{poster_link}'

printer = pprint.PrettyPrinter()


class MovieManager:
    def __init__(self, file_dir):
        with open(file_dir) as file:
            self.key = file.read()

        self.latest_id = self.__get_latest_id()

    def __get_latest_id(self):
        """get latest added movie id"""
        url = API_URL + f'movie/latest?api_key={self.key}'
        response = requests.request('GET', url)

        json = response.json()

        return json['id']

    def get_random_movie(self):
        """get a random movie by finding a random integer that not greater then the latest id"""
        movie_id = random.randint(0, self.latest_id)
        url = API_URL + f'movie/{movie_id}?api_key={self.key}'
        response = requests.request('GET', url)

        json = response.json()

        # sometimes there is no movie to an id so if that happens just find a new random id
        if 'success' in json:
            if not json['success']:
                return self.get_random_movie()

        conditions = [
            json['poster_path'] == None
        ]

        if any(conditions):
            return self.get_random_movie()

        movie = {
            'title': json['title'],
            'genres': json['genres'],
            'original_lang': json['original_language'],
            'adult': json['adult'],
            'overview': json['overview'],
            'poster_url': POSTER_URL.format(poster_link=json['poster_path'])
        }

        return movie


class Genre(Enum):
    ALL = 1
    COMEDY = 2
    ACTION = 3
    ADVENTURE = 4
    SCIENCE_FICTION = 5


class Language(Enum):
    EN = 'en-US'


if __name__ == '__main__':
    mm = MovieManager('apikey.txt')
    movie = mm.get_random_movie()
    printer.pprint(movie)
