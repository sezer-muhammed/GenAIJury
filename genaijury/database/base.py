# Interface class for database interactions
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    """
    Abstract base class defining the interface for database operations.
    """

    @abstractmethod
    def get_unique_names(self):
        """
        Retrieves a list of all unique "Name" values from the database.

        :return: A list of unique "Name" values.
        """
        pass

    @abstractmethod
    def connect(self):
        """
        Establish a connection to the database.
        """
        pass

    @abstractmethod
    def create(self, data):
        """
        Create a new record in the database.

        :param data: The data to be inserted into the database.
        """
        pass

    @abstractmethod
    def read(self, query):
        """
        Read records from the database.

        :param query: The query criteria for records to fetch.
        :return: The fetched records.
        """
        pass

    @abstractmethod
    def update(self, query, data):
        """
        Update records in the database.

        :param query: The query criteria for records to update.
        :param data: The data to update the records with.
        """
        pass

    @abstractmethod
    def delete(self, query):
        """
        Delete records from the database.

        :param query: The query criteria for records to delete.
        """
        pass
