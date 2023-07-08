import json


API_KEY = 'df0b223c&t'



def list_movies():
    with open('data.json', "r") as data:
        datamovies = json.load(data)
        # creating list to add the movies dict
        movies = []
        for movie in datamovies:
            movie = {
                'Title': movie['Title'],
                'Rating': movie['Rating'],
                'Year': movie['Year']
            }
            movies.append(movie)
        return movies


def delete_movie(title):
    file = 'data.json'
    with open(file, "r") as data:
        movies = json.load(data)
        for movie in movies:
            if title == movie['Title']:
                movies.remove(movie)

    with open(file, 'w') as json_file:
        return json.dump(movies, json_file, indent=4, separators=(',', ': '))


def add_movie(title, rating, year):
    file = 'data.json'
    with open(file, "r") as data:
        movies = json.load(data)
        # add dict to the list
        movies.append(
            {
                "Title": title,
                "Rating": rating,
                "Year": year
            }
        )
    with open(file, 'w') as json_file:
        return json.dump(movies, json_file, indent=4, separators=(',', ': '))


def update_movie(title, rating, year):
    file = 'data.json'
    with open(file, "r") as data:
        movies = json.load(data)
        for movie in movies:
            if title == movie['Title']:
                movie['Rating'] = rating
                movie['Year'] = year
    with open(file, 'w') as json_file:
        return json.dump(movies, json_file, indent=4, separators=(',', ': '))
