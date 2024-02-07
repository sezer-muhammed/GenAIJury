# Abstract base class for evaluators
from abc import ABC, abstractmethod
from genaijury.database.base import DatabaseInterface

class BaseEvaluator(ABC):
    """
    Abstract base class for evaluation strategies, initialized with a database interface.
    """

    def __init__(self, database_interface: DatabaseInterface):
        """
        Initialize the evaluator with a database interface.

        :param database_interface: An instance of a class that implements DatabaseInterface.
        """
        self.database_interface = database_interface

    @abstractmethod
    def evaluate_all(self):
        """
        Retrieves all unique entities by their "Name" field from the database,
        evaluates them based on their criteria, and calculates a score for each.

        :return: A dictionary of entity names to their evaluation scores.
        """
        pass
