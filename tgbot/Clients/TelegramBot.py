from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from tgbot.Backends.BackendInterface import BackendInterface

class TelegramBot:
    def __init__(self, backend: BackendInterface, token : str):
        self.backend = backend

        # Создаем и запускаем бота
        app = Application.builder().token(token).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("who", self.who))
        app.add_handler(CommandHandler("add", self.add_person))
        app.add_handler(CommandHandler("remove", self.remove_person))
        app.add_handler(CommandHandler("list", self.list_people))
        app.add_handler(CommandHandler("swap", self.swap_people))
        app.add_handler(CommandHandler("addlist", self.set_people_list))
        app.add_handler(CommandHandler("set", self.set_today_person))

        app.run_polling()

    # Команда /start
    async def start(self, update: Update, context: CallbackContext):
        await update.message.reply_text(
            "Привет! Этот бот помогает определить, кто сегодня разгружает посудомойку.\n"
            "Команды:\n"
            "/who — Узнать, чья очередь\n"
            "/add Имя — Добавить человека\n"
            "/addlist Имя1, Имя2, Имя3 — Добавить список людей\n"
            "/remove Имя — Удалить человека\n"
            "/list — Показать список\n"
            "/swap Имя1 Имя2 — Поменять людей местами\n"
            "/set Имя — Установить дежурного на сегодня"
        )

    # Определение, кто сегодня дежурный
    async def who(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        try:
            person = self.backend.who(chat_id)
            await update.message.reply_text(f"Сегодня очередь у {person}.")
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

    # Добавление человека в список
    async def add_person(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if not context.args:
            await update.message.reply_text("Используйте: /add Имя")
            return
        name = " ".join(context.args)

        try:
            self.backend.add_person(chat_id, name)
            await update.message.reply_text(f"Успешно добавил {name}")
        except ValueError as e:
            await update.message.reply_text(str(e))
            return


    # Удаление человека из списка
    async def remove_person(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if not context.args:
            await update.message.reply_text("Используйте: /remove Имя")
            return
        name = " ".join(context.args)
        try:
            result_msg = self.backend.remove_person(chat_id, name)
            await update.message.reply_text(result_msg)
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

    # Показ списка людей
    async def list_people(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        people = self.backend.get_list(chat_id)
        if not people:
            await update.message.reply_text("Список пуст! Добавьте людей командой /add Имя.")
            return

        list_text = "\n".join(f"{i+1}. {name}" for i, name in enumerate(people))
        await update.message.reply_text(list_text)


    # Меняем местами двух людей
    async def swap_people(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if len(context.args) < 2:
            await update.message.reply_text("Используйте: /swap Имя1 Имя2")
            return

        name1, name2 = " ".join(context.args[:1]), " ".join(context.args[1:])
        try:
            self.backend.swap_people(chat_id, name1, name2)
            await update.message.reply_text("")
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

    # Добавление списка людей
    async def set_people_list(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if not context.args:
            await update.message.reply_text("Используйте: /addlist Имя1, Имя2, Имя3")
            return
        
        names_str = " ".join(context.args)
        
        try:
            self.backend.set_people_list(chat_id, names_str)
            await update.message.reply_text("Список людей успешно добавлен!")
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

    async def set_today_person(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if not context.args:
            await update.message.reply_text("Используйте: /set Имя")
            return
        
        name = " ".join(context.args)
        
        try:
            self.backend.set_today_person(chat_id, name)
            await update.message.reply_text(f"{name} назначен(а) на сегодня!")
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

