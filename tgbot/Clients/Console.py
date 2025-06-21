import time
from tgbot.Backends.BackendInterface import BackendInterface

class Console:
    def __init__(self, backend: BackendInterface):
        self.backend = backend
        self.chat_id = 0
        self.commands = {
            "add": self.add_person,
            "remove": self.remove_person,
            "swap": self.swap_people,
            "list": self.list_people,
            "chat_id": self.set_chat_id,
            "who": self.who,
            "set": self.set_today_person,
            "setlist": self.set_people_list,
            "exit": self.exit,
        }
        self.spin()

    def spin(self):
        while True:
            command = input("Enter command (add, remove, swap, list, who, set, setlist, exit, chat_id): ").strip().lower()
            if command in self.commands:
                self.commands[command]()
            else:
                print("Unknown command. Try again.")

    def add_person(self):
        person = input("Enter name to add: ").strip()
        try:
            self.backend.add_person(self.chat_id, person)
            print(f"Добавил {person}")
        except ValueError as e:
            print(e)

    def remove_person(self):
        person = input("Enter name to remove: ").strip()
        try:
            self.backend.remove_person(self.chat_id, person)
        except ValueError as e:
            print(e)

    def swap_people(self):
        person1 = input("Enter first name: ").strip()
        person2 = input("Enter second name: ").strip()
        try:
            self.backend.swap_people(self.chat_id, person1, person2)
        except ValueError as e:
            print(e)

    def list_people(self):
        people = self.backend.get_list(self.chat_id)
        if not people:
            print("List is empty!")
        else:
            print("Current list:")
            for person in people:
                print(f"- {person}")

    def set_chat_id(self):
        self.chat_id = input("Enter chat id: ").strip()

    def exit(self):
        print("Goodbye!")
        exit(0)

    def who(self):
        try:
            person = self.backend.who(self.chat_id)
            print(f"Today's person is: {person}")
        except ValueError as e:
            print(e)

    def set_today_person(self):
        person = input("Enter name to set as today's person: ").strip()
        try:
            self.backend.set_today_person(self.chat_id, person)
            print(f"{person} is set as today's person")
        except ValueError as e:
            print(e)

    def set_people_list(self):
        print("Enter list of names (comma-separated):")
        names_input = input().strip()
        
        try:
            self.backend.set_people_list(self.chat_id, names_input)
            print("List set successfully!")
            # Show the new list
            self.list_people()
        except ValueError as e:
            print(e)
