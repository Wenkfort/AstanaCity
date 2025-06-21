from datetime import date
from tgbot.DataBase.DataBaseInterface import DataBaseInterface
from tgbot.Backends.BackendInterface import BackendInterface

BASE_DATA = date(2024, 1, 1)

class BackendReal(BackendInterface):
    def __init__(self, data_worker: DataBaseInterface):
        super().__init__()
        self.data_worker = data_worker

    def who(self, chat_id) -> str:
        people = []
        try:
            # Get people in their stored order from database
            people = self.data_worker.get_persons(chat_id)
        except Exception as e:
            raise ValueError(f"Ошибка при получении списка: {str(e)}")
        
        if not people:
            raise ValueError("Список пуст! Добавьте людей.")

        index = self.__get_index(people)
        person = people[index]
        return person

    def add_person(self, chat_id, name):
        self.data_worker.add_person(chat_id, name)

    def remove_person(self, chat_id, name):
        self.data_worker.remove_person(chat_id, name)

    def swap_people(self, chat_id, person1, person2):
        try:
            people = self.data_worker.get_persons(chat_id)
            if person1 not in people or person2 not in people:
                raise ValueError("Один или оба человека не найдены в списке!")
            
            # Clear the list for this chat
            self.data_worker.clear_chat(chat_id=chat_id)
            
            # Swap positions
            for i, person in enumerate(people):
                if person == person1:
                    people[i] = person2
                elif person == person2:
                    people[i] = person1
            
            # Add back in new order
            for person in people:
                self.data_worker.add_person(chat_id, person)
            
        except Exception as e:
            raise ValueError(f"Ошибка при обмене местами: {str(e)}")

    def get_list(self, chat_id) -> list:
        return self.data_worker.get_persons(chat_id)

    def set_today_person(self, chat_id, name):
        try:
            # Get current order
            people = self.data_worker.get_persons(chat_id)
            if name not in people:
                raise ValueError(f"{name} не найден в списке!")
            
            # Calculate current and target indices
            current_index = people.index(name)
            target_index = self.__get_index(people)
            
            # Calculate how many positions to shift
            shift = (current_index - target_index) % len(people)
            
            if shift != 0:
                # Create new order by rotating the list
                new_order = people[shift:] + people[:shift]
                # Update the database with new order
                self.data_worker.reorder_people(chat_id, new_order)
            
        except Exception as e:
            raise ValueError(f"Ошибка при установке дежурного: {str(e)}")

    def set_people_list(self, chat_id, names_str):
        """Set a new list of people, replacing the existing one"""
        try:
            # Split the string by commas and clean up whitespace
            names = [name.strip() for name in names_str.split(' ')]
            # Remove empty names
            names = [name for name in names if name]

            if not names:
                raise ValueError("Список пуст! Используйте формат: Имя1 Имя2 Имя3")
            
            # Clear existing list
            self.data_worker.clear_chat(chat_id)
            
            # Add all names in the specified order
            for name in names:
                self.data_worker.add_person(chat_id, name)
            
        except Exception as e:
            raise ValueError(f"Ошибка при установке списка: {str(e)}")

    def __get_index(self, people):
        today = date.today()
        days_since_base = (today - BASE_DATA).days
        return days_since_base % len(people)
