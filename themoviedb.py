import requests


class TheMovieDB:
    def __init__(self):
        api_auth = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZjQ4MTI1Zjk2ZjA2Y2YwYmEyZGIxZmFkYmY2NjA0NSIsInN1YiI6IjY0ODU1MTNkOTkyNTljMDBhY2NjZmVhYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.gGm7e4Ann9bsXz-RG28FYuHYtQ_AtpWubdn0D8IruvY"
        self.headers = {
            "accept": "application/json",
            "Authorization": api_auth
        }

    def get_movie_list(self, name):
        url = "https://api.themoviedb.org/3/search/movie"
        parm = {
            "query": name
        }

        response = requests.get(url=url, headers=self.headers, params=parm)
        response = response.json()["results"]
        return response
