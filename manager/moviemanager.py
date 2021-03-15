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

        self.temp_movie = self.find_random_movie()

        self.random_movie_cashe = []
        # adding a movie to make sure its not empty
        self.random_movie_cashe.append(self.find_random_movie())

        # starting a thread to add movies in the background
        threading.Thread(target=self.load_random_movies).start()

    def load_random_movies(self):
        while True:
            if len(self.random_movie_cashe) < MOVIE_CASHE_LEN:
                self.random_movie_cashe.append(self.find_random_movie())

    def get_random_movie(self):
        movie = self.random_movie_cashe.pop(0)
        return movie

    def find_random_movie(self):
        """get a random movie by finding a random integer that not greater then the latest id"""
        movie_id = random.randint(0, self.latest_id)
        url = API_URL + f'movie/{movie_id}?api_key={self.key}'
        response = requests.request('GET', url)

        json = response.json()

        # sometimes there is no movie to an id so if that happens just find a new random id
        if 'success' in json:
            if not json['success']:
                return self.find_random_movie()

        conditions = [
            json['poster_path'] is None,
            json['adult'] is True
        ]

        if any(conditions):
            return self.find_random_movie()

        movie = {
            'title': json['title'],
            'genres': json['genres'],
            'original_lang': json['original_language'],
            'overview': json['overview'],
            'poster_url': POSTER_URL.format(poster_link=json['poster_path'])
        }

        return movie

    def __get_latest_id(self):
        """get latest added movie id"""
        url = API_URL + f'movie/latest?api_key={self.key}'
        response = requests.request('GET', url)

        json = response.json()

        return json['id']

if __name__ == '__main__':
    mm = MovieManager('apikey.txt')
    movie = mm.get_random_movie()
    printer.pprint(movie)
