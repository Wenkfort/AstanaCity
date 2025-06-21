from abc import ABC, abstractmethod

class BackendInterface(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def who(self, chat_id) -> str:
        return ""

    @abstractmethod
    def add_person(self, chat_id, person):
        pass

    @abstractmethod
    def remove_person(self, chat_id, person):
        pass

    @abstractmethod
    def swap_people(self, chat_id, person1, person2):
        pass

    @abstractmethod
    def get_list(self, chat_id) -> list:
        return []
