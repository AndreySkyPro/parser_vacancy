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


class AbstractJson(ABC):

    @abstractmethod
    def create_file(self):
        pass

    @abstractmethod
    def load_file(self):
        pass
