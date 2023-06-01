from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_vacansies(self):
        pass

    @abstractmethod
    def validate_vacansies(self):
        pass

