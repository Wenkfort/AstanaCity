import os
from tgbot.Clients.Console import Console
from tgbot.Clients.TelegramBot import TelegramBot
from tgbot.Backends.BackendReal import BackendReal
from tgbot.DataBase.DataBasePostreSQL import DataBasePostgreSQL
from tgbot.DataBase.DataBaseJson import DataBaseJson

TYPE = os.environ.get("TYPE", "LOCAL")
DATABASE_TYPE = os.environ.get("DATABASE_TYPE", "POSTGRESQL")
TOKEN = os.environ.get("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "")
DATA_FILE = os.environ.get("DATA_FILE", "data.json")

if __name__== "__main__":
    if TYPE is None:
        print("Set TYPE environment variable. Choose one of possible types: LOCAL, TELEGRAM")

    client = None

    if DATABASE_TYPE == "POSTGRESQL":
        data_worker = DataBasePostgreSQL(DATABASE_URL)
    elif DATABASE_TYPE == "JSON":
        data_worker = DataBaseJson(DATA_FILE)
    else:
        raise ValueError("Invalid database type")

    backend = BackendReal(data_worker)

    if TYPE == "LOCAL":
        client = Console(backend)
    if TYPE == "TELEGRAM":
        client = TelegramBot(backend, TOKEN)
    else:
        raise ValueError("Invalid type")
