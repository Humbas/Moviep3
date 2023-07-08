from istorage import IStorage
import csv
from csv import DictWriter


class StorageCSV(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        file = 'data.csv'
        with open(file, "r") as data:
            field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
            datamovies = csv.DictReader(data, fieldnames=field_names)
            movie_list = list(datamovies)
            return movie_list

    def add_movie(self, new_movie):
        file = 'data.csv'
        with open(file, "r") as data:
            datamovies = csv.DictReader(data)
            movie_list = list(datamovies)
            if new_movie not in movie_list:
                movie_list.append(new_movie)
            movie_list
        field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
        with open(file, 'a') as updated_file:
            new_object = DictWriter(updated_file, fieldnames=field_names)
            new_object.writerow(new_movie)
            updated_file.close()

    def check_if_movie_exists(self, movie_title, movie_year):
        file = 'data.csv'
        with open(file, "r") as data:
            field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
            datamovies = csv.DictReader(data, fieldnames=field_names)
            movie_list = list(datamovies)
            for movie in movie_list:
                if movie_title in movie['Title'] and movie_year in movie['Year']:
                    return True

    def delete_from_repeated_titles(self, movie_title, year):
        file = 'data.csv'
        with open(file, "r") as data:
            with open(file, "r") as data:
                field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
                datamovies = csv.DictReader(data, fieldnames=field_names)
                movie_list = list(datamovies)
                for movie in movie_list:
                    if movie_title == movie['Title'] and year == movie['Year']:
                        movie_list.remove(movie)
                updated_file = open(file, 'w')
                writer = csv.writer(updated_file)
                for movie in movie_list:
                    writer.writerow(movie.values())
                updated_file.close()

    def delete_movie(self, movie_title):
        file = 'data.csv'
        with open(file, "r") as data:
            field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
            datamovies = csv.DictReader(data, fieldnames=field_names)
            movie_list = list(datamovies)
            for movie in movie_list:
                if movie_title == movie['Title']:
                    movie_list.remove(movie)
            updated_file = open(file, 'w')
            writer = csv.writer(updated_file)
            for movie in movie_list:
                if movie['Title'] != movie_title:
                    writer.writerow(movie.values())
            updated_file.close()

    def update_movie_repeated(self, title, rating, year, plot, old_year):
        file = 'data.csv'
        with open(file, "r") as data:
            field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
            datamovies = csv.DictReader(data, fieldnames=field_names)
            movie_list = list(datamovies)
            year = str(year)
            year = year[0:4]
            old_year = str(old_year)
            for movie in movie_list:
                if title == movie['Title'] and old_year == movie['Year']:
                    movie['Rating'] = rating
                    movie['Year'] = year
                    movie['Plot'] = plot
            updated_file = open(file, 'w')
            writer = csv.writer(updated_file)
            for movie in movie_list:
                writer.writerow(movie.values())
            updated_file.close()

    def update_movie(self, title, rating, year, plot):
        file = 'data.csv'
        with open(file, "r") as data:
            field_names = ['Title', 'Year', 'Rating', 'Photo', 'Plot', 'IMDB']
            datamovies = csv.DictReader(data, fieldnames=field_names)
            movie_list = list(datamovies)
            year = str(year)
            year = year[0:4]
            for movie in movie_list:
                if title == movie['Title']:
                    movie['Rating'] = rating
                    movie['Year'] = year
                    movie['Plot'] = plot
            updated_file = open(file, 'w')
            writer = csv.writer(updated_file)
            for movie in movie_list:
                writer.writerow(movie.values())
            updated_file.close()
