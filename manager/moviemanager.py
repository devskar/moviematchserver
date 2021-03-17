import threading
import requests
import random
import pprint

API_URL = 'https://api.themoviedb.org/3/'
POSTER_URL = 'https://image.tmdb.org/t/p/w500{poster_link}'

MOVIE_CASHE_LEN = 10

printer = pprint.PrettyPrinter()


class MovieManager:
    def __init__(self, file_dir):
        with open(file_dir) as file:
            self.key = file.read()

        self.latest_id = self.__get_latest_id()

        self.random_movie_cashe = set()
        # adding a movie to make sure its not empty
        self.random_movie_cashe |= self.find_random_movies(MOVIE_CASHE_LEN)

    def find_random_movies(self, amount):
        """get random movies by finding a random integer that is smaller then the latest id"""

        movies = set()

        for n in range(amount):

            json = self.get_valid_movie()

            movie = Movie.from_json(json)

            if movie in movies:
                continue

            movies.add(movie)

        return movies

    def get_valid_movie(self, adult=False):

        json = self.get_random_movie()

        # sometimes there is no movie to an id so if that happens just find a new random id
        if 'success' in json:
            if not json['success']:
                return self.get_valid_movie()

        conditions = [
            json['poster_path'] is None,
            json['adult'] is not adult
        ]

        if any(conditions):
            return self.get_valid_movie()
        return json

    def get_random_movie(self):
        movie_id = random.randint(0, self.latest_id)
        return self.get_movie_by_id(movie_id)

    def get_movie_by_id(self, movie_id):
        url = API_URL + f'movie/{movie_id}?api_key={self.key}'

        response = requests.request('GET', url)

        return response.json()

    def find_movie_with_genres(self, amount, **genres):
        pass

    def __get_latest_id(self):
        """get latest added movie id"""
        url = API_URL + f'movie/latest?api_key={self.key}'
        response = requests.request('GET', url)

        json = response.json()

        return json['id']


class Movie:

    def __init__(self, id, title, genres, original_language, overview, posterpath):
        self.id = id
        self.title = title
        self.genres = genres
        self.original_language = original_language
        self.overview = overview
        self.poster_url = POSTER_URL.format(poster_link=posterpath)

    def get_as_dict(self):
        return {
            'title': self.title,
            'genres': self.genres,
            'original_lang': self.original_language,
            'overview': self.overview,
            'poster_url': self.poster_url
        }

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.id == other.id
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def from_json(json):
        return Movie(json['id'], json['title'], json['genres'], json['original_language'], json['overview'],
                     json['poster_path'])

if __name__ == '__main__':
    mm = MovieManager('apikey.txt')
    print(len(mm.random_movie_cashe))
