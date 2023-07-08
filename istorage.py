"""
This module defines an abstract base class (ABC) that serves as an interface
"""
from abc import ABC, abstractmethod


class IStorage(ABC):
    """
     defines a generic interface for movie storage.
      """

    @abstractmethod
    def list_movies(self) -> dict:
        """
                Abstract method that returns a movie dict list.
        """

        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster) -> None:
        """
             Abstract method that adds a movie to the storage.
             searches online database by user input and takes for
             the database json or csv exact matches.
             Parameters: Title, Year, Rating, Photo, Plot and IMDB
        """
        pass

    @abstractmethod
    def delete_movie(self, title) -> None:
        """
             Abstract method that deletes a movie from storage
             uses Title parameter for seatrch and if the Title is repeated asks also
             for year
        """
        pass

    @abstractmethod
    def update_movie(self, title, notes) -> None:
        """
               Abstract method that updates movie from storage
               uses Title parameter for search and if the Title is repeated asks also
               for year
          """
        pass
