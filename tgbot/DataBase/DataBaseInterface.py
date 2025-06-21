from abc import ABC, abstractmethod

class DataBaseInterface(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_persons(self, chat_id):
        pass

    @abstractmethod
    def add_person(self, chat_id, name):
        pass

    @abstractmethod
    def remove_person(self, chat_id, name):
        pass

    @abstractmethod
    def clear_chat(self, chat_id):
        pass

    @abstractmethod
    def set_people_list(self, chat_id, names):
        pass