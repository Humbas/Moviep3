from istorage import IStorage
import acessory_functions
import requests
from fuzzywuzzy import fuzz  # fuzzy library
import random
import statistics


class MovieApp:
    """ provides a command-line interface for users to perform app tasks"""

    def __init__(self, storage: IStorage):
        self._storage = storage

    def _input_year_select(self, year_list, user_title):
        """ if there are more than one equal Titles, allows the user to choose by year to delete"""
        input_year = int(input(f"Enter the year of the {user_title} films you wish to delete: "))
        confirmation = str(input("Are you sure you wanna delete this movie? If so write Yes :"))
        if input_year:
            if input_year not in year_list:
                acessory_functions.warning("This is not an available year for this movie")
                return False
            if confirmation == 'Yes' or confirmation == 'yes':
                input_year = str(input_year)
                self._storage.delete_from_repeated_titles(user_title, input_year)
                acessory_functions.done("Successfully deleted!")
                return True
            if confirmation != 'Yes' or confirmation != 'No':
                acessory_functions.warning(
                    "What are you doing? Please write Yes if you wanna delete this movie")
                return False
        else:
            acessory_functions.warning("Enter a year!")

    def _input_year_control(self, input_year, year_list, user_title):
        """ if there are more than one equal Titles, allows the user to choose by year to update"""
        if input_year not in year_list:
            acessory_functions.warning(
                f"{input_year} not among the films")
            return False
        else:
            new_rating = input(
                f'Provide {user_title} released in {input_year} with a new rating between 1 - 10 :')
            new_rating = float(new_rating.replace('%', ''))
            new_year = int(input(
                f'Also provide {user_title} released in {input_year}  with a new release year : '))
            new_plot = str(
                input(f'Also provide {user_title} released in {input_year}  with a new plot: '))
            new_year = str(new_year)
            self._storage.update_movie_repeated(user_title, new_rating, new_year, new_plot, input_year)
            acessory_functions.done(f"movie {user_title} successfully updated! \n")
            return True

    def _display_results(self, movie_list, user_title, method_name, attached_list):
        """Display search results"""
        acessory_functions.done(f"{method_name} {user_title} results:")
        if len(movie_list) > 0:
            for movie in movie_list:
                if self._storage.check_if_movie_exists(movie['Title'], movie['Year']):
                    acessory_functions.done(
                        f"{movie['Title']}, with the Internet movie database rating of {movie['Rating']} released in {movie['Year']} exists in our"
                        f"database.")
                else:
                    acessory_functions.done(
                        f"{movie['Title']} with the Internet movie database rating of {movie['Rating']}, released "
                        f" in {movie['Year']} with the plot: {movie['Plot']}")
                    attached_list.append(movie['Title'])
            print("\n")

    def _find_movie(self, list_movies, movie_name, name_list):
        """compares user input with database"""
        for movie in list_movies:
            title = movie['Title']
            name_list.append(title)
        matches = fuzz.partial_ratio(movie_name.lower(), title.lower())
        if matches == 100 and movie_name != title:
            acessory_functions.warning(f"We dont have a movie called {movie_name} do you mean:")
            return False
        if title == movie_name:
            acessory_functions.done(
                f"We do have a movie called {movie_name} with the rating of {movie['Rating']} released in {movie['Year']} with the plot: {movie['Plot']}")
            return True
        if title != movie_name and matches != 100:
            acessory_functions.warning(str(movie_name) + " movie does not exist ")
            return False

    def _command_list_movies(self) -> dict:
        """shows movie list"""
        acessory_functions.done(f"We currently have {len(self._storage.list_movies())} movies avaiable \n")
        for movie in self._storage.list_movies():
            acessory_functions.done(
                movie['Title'] + " with the ImDB rating of " + str(movie['Rating']) + " released in " + str(
                    movie['Year']) + " and with the plot: " + str(movie['Plot']))

    def _command_add_movie(self) -> None:
        while True:
            try:
                print("\n")
                user_title = str(input("Enter a movie title to search and add. Write exit to leave: "))
                url_movie = f'https://omdbapi.com/?apikey={acessory_functions.API_KEY}&s={user_title}'
                data = requests.get(url_movie)
                data.raise_for_status()
                response = requests.get(url_movie).json()
                movies_found = response['Search']
                number_of_movies = len(movies_found)
                if user_title == 'Exit' or user_title == 'exit':
                    break
                if movies_found:
                    acessory_functions.done(f"We have found {number_of_movies} results related to {user_title}\n")
                    partial_matches = []
                    exact_matches = []
                    list_titles = []
                    total_movies = []
                    matches_list = []
                    partial_list = []
                    for movie in movies_found:
                        movie_id = movie['imdbID']
                        """using another dict to access more movie data"""
                        more_movie_data = f'http://www.omdbapi.com/?apikey={acessory_functions.API_KEY}&i={movie_id}&plot=short&r=json'
                        movie_data_dict = requests.get(more_movie_data).json()
                        rating = movie_data_dict['imdbRating']
                        rating = float(rating)
                        plot = movie_data_dict['Plot']
                        movie_title = movie_data_dict['Title']
                        year = movie_data_dict['Year']
                        photo = movie_data_dict['Poster']
                        result = {
                            'Title': movie_title,
                            'Year': year,
                            'Rating': rating,
                            'Photo': photo,
                            'Plot': plot,
                            'IMDB': movie_id
                        }
                        list_titles.append(movie_title)
                        total_movies.append(result)
                        user_match = fuzz.ratio(user_title.lower(), movie_title.lower())
                        if user_match == 100:
                            exact_matches.append(result)
                        else:
                            partial_matches.append(result)

                    self._display_results(exact_matches, user_title, 'Exact', matches_list)
                    print("\n")
                    self._display_results(partial_matches, user_title, 'Partial', partial_list)

                    for movie in total_movies:
                        if user_title == movie['Title']:
                            if acessory_functions.count_titles(matches_list,
                                                               movie['Title']) > 1 or acessory_functions.count_titles(
                                partial_list, movie['Title']) > 1:
                                acessory_functions.done(
                                    f"Could it be {movie['Title']} released in {movie['Year']} with the Internet movie database rating of {movie['Rating']}?")
                                year_confirmation = int(
                                    input(
                                        f"Since there are several {movie['Title']} movies, insert the year to be sure: "))
                                if not isinstance(year_confirmation, int):
                                    acessory_functions.warning(f"Hey, write a proper year!")
                                else:
                                    if self._storage.check_if_movie_exists(movie['Title'], movie['Year']):
                                        acessory_functions.warning(
                                            f"We have {movie['Title']} released in {movie['Year']} already, please consult the result list")
                                    elif str(year_confirmation) != movie['Year']:
                                        acessory_functions.warning(
                                            f"This year is not among the available years!")
                                    else:
                                        self._storage.add_movie(movie)
                                        acessory_functions.done(f"{movie['Title']} successfully added!")
                                        break

                            elif acessory_functions.count_titles(partial_list, movie[
                                'Title']) == 1 or acessory_functions.count_titles(matches_list, movie['Title']) == 1:
                                confirmation = str(input(f"You mean {movie['Title']} released in {movie['Year']}? if "
                                                         f"so write yes:"))
                                if confirmation == 'Yes' or confirmation == 'yes':
                                    if self._storage.check_if_movie_exists(movie['Title'], movie['Year']):
                                        acessory_functions.warning(
                                            f"We have {movie['Title']} released in {movie['Year']} already, please consult the result list")
                                    else:
                                        self._storage.add_movie(movie)
                                        acessory_functions.done(f"{movie['Title']} successfully added!")
                                        break

                        else:
                            matches = fuzz.partial_ratio(user_title.lower(), movie['Title'].lower())
                            if matches == 100:
                                acessory_functions.done(f"Do you mean {movie['Title']} released in {movie['Year']} ?")
                else:
                    acessory_functions.warning(f"{user_title} not found")
            except KeyError:
                acessory_functions.warning(f"Dude, what is {user_title}? We never eared of this movie. Try again")

    def _command_update_movie(self) -> None:
        """allows update year, rating and plot"""
        while True:
            try:
                name_list = []
                list_movies = self._storage.list_movies()
                if len(self._storage.list_movies()) > 0:
                    acessory_functions.done("These are the available movies we have right now:\n")
                    for movie in self._storage.list_movies():
                        movie_titles = movie['Title']
                        name_list.append(movie_titles)
                        acessory_functions.done(
                            movie['Title'] + " with the ImDB rating of " + str(movie['Rating']) + " released in " + str(
                                movie['Year']) + " and with the plot: " + str(movie['Plot']))
                    acessory_functions.done("\n")
                else:
                    acessory_functions.warning("There are no movies available to show ")
                user_title = input("Enter a movie title to update. To leave simply write exit : ")
                if 'Exit' not in name_list:
                    if user_title == 'Exit' or user_title == 'exit' and user_title not in name_list:
                        break
                movie_titles = []  # this list will store titles for input control
                for movie in list_movies:
                    movie_title = movie["Title"]
                    movie_titles.append(movie_title)
                if user_title in movie_titles:
                    if acessory_functions.count_movies(movie_titles, user_title) > 1:
                        years = []
                        acessory_functions.done(
                            f"We actually have {acessory_functions.count_movies(movie_titles, user_title)}  movies  named {user_title}")
                        acessory_functions.done("They are as follows: \n")
                        for movie in list_movies:
                            if user_title in movie['Title']:
                                """making sure its a 4 digit string"""
                                year = movie['Year'][0:4]
                                year = int(year)
                                years.append(year)
                                acessory_functions.done(f"{user_title} released in {movie['Year']}")
                        acessory_functions.done("Which one you wanna update?")
                        input_year = int(input(f"Enter the year of the {user_title} films you wish to update: "))
                        self._input_year_control(input_year, years, user_title)
                    else:

                        new_rating = input(
                            f'Provide {user_title} with a new rating between 1 - 10 :')
                        new_rating = float(new_rating.replace('%', ''))
                        new_year = int(input(
                            f'Also provide {user_title}  with a new release year : '))
                        new_plot = str(
                            input(f'Also provide {user_title} released  with a new plot: '))
                        self._storage.update_movie(user_title, new_rating, new_year, new_plot)
                        acessory_functions.done(f"movie {user_title} successfully updated! \n")
                else:
                    acessory_functions.warning(str(user_title) + " does not  exist, restart")
            except ValueError:
                acessory_functions.warning("Insert proper year!")

    def _command_delete_movie(self) -> None:
        """deletes movie by title """
        while True:
            try:
                list_movies = self._storage.list_movies()
                name_list = []
                if len(list_movies) > 0:
                    acessory_functions.done("These are the available movies we have right now:\n")
                    for movie in list_movies:
                        movie_titles = movie['Title']
                        name_list.append(movie_titles)
                        acessory_functions.done(
                            movie['Title'] + " with the ImDB rating of " + str(movie['Rating']) + " released in " + str(
                                movie['Year']) + " and with the plot: " + str(movie['Plot']))
                    acessory_functions.done("\n")
                else:
                    acessory_functions.warning("There are no movies available to show ")
                user_title = input("Enter a movie title to delete. To leave simply write exit : ")
                if 'Exit' not in name_list:
                    if user_title == 'Exit' or user_title == 'exit' and user_title not in name_list:
                        break
                movie_titles = []
                for movie in list_movies:
                    movie_title = movie["Title"]
                    movie_titles.append(movie_title)
                if user_title in movie_titles:
                    if acessory_functions.count_movies(movie_titles, user_title) > 1:
                        years = []
                        acessory_functions.done(
                            f"We actually have {acessory_functions.count_movies(movie_titles, user_title)}  movies  named {user_title}")
                        print("They are as follows: \n")
                        for movie in list_movies:
                            if user_title in movie['Title']:
                                year = movie['Year'][0:4]
                                year = int(year)
                                years.append(year)
                                print(f"{user_title} released in {movie['Year']}")
                        acessory_functions.done("Which one you wanna delete?")
                        self._input_year_select(years, user_title)
                    else:
                        confirmation = str(input("Are you sure you wanna delete this movie? If so write Yes :"))
                        if confirmation == 'Yes' or confirmation == 'yes':
                            self._storage.delete_movie(user_title)
                            acessory_functions.done(f"movie {user_title} successfully deleted! \n")
                else:
                    acessory_functions.warning(str(user_title) + " does not  exist, restart")
            except ValueError:
                acessory_functions.warning("Insert proper year")

    def _command_movie_stats(self) -> None:
        """display worst, best movie, average and medium ratting """
        list_movies = self._storage.list_movies()
        sum_values = 0
        value_list = []
        sum_of_movies = len(list_movies)
        acessory_functions.done("Here we have the movie list status:")
        acessory_functions.done(f"Currently we have {sum_of_movies} available movies")
        for movie in list_movies:
            rating = movie['Rating']
            rating = float(rating)
            sum_values += rating
            rating_int = float(rating)
            value_list.append(rating_int)
        average = sum_values / sum_of_movies
        medium = statistics.median(value_list)
        best_score = max(value_list)
        worse_score = min(value_list)
        for movie in list_movies:
            rating = float(movie['Rating'])
            if rating == best_score:
                acessory_functions.done(
                    f"The best movie is {movie['Title']}  released in {movie['Year']} with the ImDB score of {best_score}")
            if rating == worse_score:
                acessory_functions.done(
                    f"The worse movie is {movie['Title']} released in {movie['Year']} with the ImDB score of {worse_score}")
        acessory_functions.done(f"The average ImDB rating is {average}")
        acessory_functions.done(f"The median ratting of the movie list is {medium}")

    def _command_random_movie(self) -> None:
        """random movie"""
        list_movies = self._storage.list_movies()
        choice = random.choice(list_movies)
        acessory_functions.done(
            str(choice['Title']) + " with the rating of " + str(choice['Rating']) + " released in " + str(
                choice['Year']) + " is a random movie from the list")

    def _command_search_movie(self) -> None:
        """search database """
        while True:
            name_list = []
            list_movies = self._storage.list_movies()
            movie_name = str(input(
                "Please enter a part of a movie name title or an entire title. Write exit to stop searching: "))
            if 'Exit' not in name_list:
                if movie_name == 'Exit' or movie_name == 'exit' and movie_name not in name_list:
                    break
            self._find_movie(list_movies, movie_name, name_list)

    def _command_sort_movie(self):
        """sort by rating """
        self.list_movies = storage.list_movies()
        acessory_functions.done("Movies sorted by ranking from best to worse:")
        sorted_list = sorted(self.list_movies, key=lambda x: x['Rating'], reverse=True)
        for movie in sorted_list:
            acessory_functions.done(
                str(movie['Title']) + " with the ImDB rating of " + str(movie['Rating']) + " released in " + str(
                    movie['Year']))

    def _command_generate_website(self):
        """generate webpage """
        self.list_movies = storage.list_movies()
        output = f'<div class="list-movies-title"><h1>Humbertos Movie App</h1></div><div><ol class="movie-grid">'
        for movie in self.list_movies:
            title = movie['Title']
            rating = movie['Rating']
            photo = movie['Photo']
            year = movie['Year']
            imdb = movie['IMDB']
            movie_url = 'http://www.imdb.com/title/' + str(imdb)
            output += '<li><a href="' + str(movie_url) + '" Title = "' + str(title) + '  ' + str(
                year) + '"><img src="' + str(
                photo) + '" alt="' + str(title) + '"  " \
                                                                                                          "Title="' + str(
                title) + '  ' + str(year) + '" /></a><span class="movie-title" style="text-align:center">' + str(
                title) + '</span><br/><span class="movie-year" style="text-align:center;">' + str(
                year) + '</span></span><br/><span class="movie-year" style="text-align:center;">' + str(
                rating) + '</span></li>'
        output += '</ol></div>'
        html_page_data = acessory_functions.read_file("../_static/index_template.html")
        html_page_movies = html_page_data.replace("__MOVIES__", output)
        acessory_functions.write_file("../_static/index.html", html_page_movies)
        acessory_functions.done("Website successfully created!")

    def run(self):
        acessory_functions.done("*********** My Movies database ********** \n")
        acessory_functions.done("Menu: ")
        acessory_functions.done("0. Exit")
        acessory_functions.done("1. List Movies")
        acessory_functions.done("2. Add movie")
        acessory_functions.done("3. Delete movie")
        acessory_functions.done("4. Update movie")
        acessory_functions.done("5. Stats")
        acessory_functions.done("6. Random movie")
        acessory_functions.done("7. Search movie")
        acessory_functions.done("8. Movies sorted by rating")
        acessory_functions.done("9. Generate website \n")

        while True:
            try:
                number = int(input("Enter choice (0-9) : "))
                if number == 0:
                    return exit()
                elif number == 1:
                    self._command_list_movies()
                elif number == 2:
                    self._command_add_movie()
                elif number == 3:
                    self._command_delete_movie()
                elif number == 4:
                    self._command_update_movie()
                elif number == 5:
                    self._command_movie_stats()
                elif number == 6:
                    self._command_random_movie()
                elif number == 7:
                    self._command_search_movie()
                elif number == 8:
                    self._command_sort_movie()
                elif number == 9:
                    self._command_generate_website()
                else:
                    acessory_functions.warning(str(number) + " its not a number available in the menu")
            except ValueError:
                acessory_functions.warning("Insert a number between 0 and 9, not characters!!!")


if __name__ == "__main__":
    import storage_csv

    storage = storage_csv.StorageCSV('data.csv')
    movie_app = MovieApp(storage)
    movie_app.run()
