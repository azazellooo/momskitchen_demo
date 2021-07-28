from bot.handlers.main_commands import MainCommandsHandler
from bot.telegram_bot import TelegramBot


class KitchenBotProvider(TelegramBot):
    def __init__(self):
        super(KitchenBotProvider, self).__init__()
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

    def add_handlers(self):
        MainCommandsHandler(self.dispatcher)
