from tgbot.Backends.BackendInterface import BackendInterface

class NullBackend(BackendInterface):
    def __init__(self):
        super().__init__()
        self.index = 0

    def who(self, chat_id) -> str:
        answer = "bot id: " + str(self.index)
        self.index += 1
        return answer

    def add_person(self, chat_id, person):
        self.index += 1

    def remove_person(self, chat_id, person):
        self.index -= 1

    def swap_people(self, chat_id, person1, person2):
        self.index = 0

    def get_list(self):
        return []
    