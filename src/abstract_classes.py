from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_vacansies(self):
        pass


class AbstractJson(ABC):

    @abstractmethod
    def create_jfile(self):
        pass

    @abstractmethod
    def load_jfile(self):
        pass
