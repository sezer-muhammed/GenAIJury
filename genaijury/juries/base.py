# Abstract base class for juries
from abc import ABC, abstractmethod

class BaseJury(ABC):
    def __init__(self, api_key: str, database, jury_history: str, jury_perspective: str):
        """
        Initialize the jury with common attributes.

        :param api_key: API key for accessing external services.
        :param database: A reference to the database object for storing and retrieving data.
        :param jury_history: A string describing the history of the jury, used for personality.
        :param jury_perspective: A string defining the jury's perspective, used for personality.
        """
        self.api_key = api_key
        self.database = database
        self.jury_history = jury_history
        self.jury_perspective = jury_perspective

    def prepare_prompt(self, criteria: dict) -> str:
        """
        Prepare the evaluation prompt based on the criteria, history, and perspective.

        :param criteria: A dictionary of criteria for evaluation.
        :return: A string prompt for the evaluation.
        """
        # This method can be customized or overridden by subclasses if needed.
        # For now, it's a placeholder to illustrate potential functionality.
        prompt = f"Considering the history: {self.jury_history} and perspective: {self.jury_perspective}, evaluate the following criteria: {criteria}"
        return prompt

    @abstractmethod
    def evaluate(self, data) -> dict:
        """
        Evaluate the given data against the set criteria. This method must be implemented by all subclasses.

        :param data: The data to be evaluated.
        :return: A dictionary containing the evaluation results.
        """
        pass
