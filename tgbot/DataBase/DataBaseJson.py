import json
import os
from tgbot.DataBase.DataBaseInterface import DataBaseInterface

class DataBaseJson(DataBaseInterface):
    def __init__(self, data_file):
        super().__init__()
        self.data_file = data_file

    def add_person(self, chat_id, name):
        data = self.__load_data()
        chat_id_str = str(chat_id)
        
        if chat_id_str not in data:
            data[chat_id_str] = []
            
        if name in data[chat_id_str]:
            raise ValueError(f"{name} уже в списке!")
            
        data[chat_id_str].append(name)
        self.__save_data(data)

    def remove_person(self, chat_id, name):
        data = self.__load_data()
        chat_id_str = str(chat_id)
        
        if chat_id_str not in data:
            raise ValueError(f"{name} нет в списке!")
            
        if name not in data[chat_id_str]:
            raise ValueError(f"{name} нет в списке!")
            
        data[chat_id_str].remove(name)
        self.__save_data(data)

    def get_persons(self, chat_id):
        data = self.__load_data()
        chat_id_str = str(chat_id)
        
        if chat_id_str not in data:
            return []
            
        return data[chat_id_str]
    
    def clear_chat(self, chat_id):
        data = self.__load_data()
        chat_id_str = str(chat_id)
        
        if chat_id_str in data:
            data[chat_id_str] = []
            self.__save_data(data)

    def set_people_list(self, chat_id, names):
        data = self.__load_data()
        chat_id_str = str(chat_id)
        
        if chat_id_str not in data:
            data[chat_id_str] = []
            
        for name in names:
            if name not in data[chat_id_str]:
                data[chat_id_str].append(name)
                
        self.__save_data(data)

    def __load_data(self):
        """Load all lists from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def __save_data(self, data):
        """Save data to file"""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
