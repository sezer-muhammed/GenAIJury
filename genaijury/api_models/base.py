from abc import ABC, abstractmethod

class APIModel(ABC):
    @abstractmethod
    def __init__(self):
        """
        Initialize the API model with necessary configuration.
        This method should set up any required attributes for the API call, such as API keys or base URLs.
        """
        pass

    @abstractmethod
    def configure(self, api_key: str, **config):
      """
      Configure the API model with dynamic parameters.

      :param config: A dictionary or set of keyword arguments containing additional configuration parameters.
          api_key: The API key required for authentication.
      """
      pass

    @abstractmethod
    def call(self, prompt: str) -> str:
        """
        Make an API call with the given prompt.
        :param prompt: The prompt to send to the API.
        :return: The API's response as a string.
        """
        pass
