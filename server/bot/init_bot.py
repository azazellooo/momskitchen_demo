from bot.bot_provider import KitchenBotProvider


class BotInit():
    def __init__(self):
        self.bot = KitchenBotProvider()

    def launch(self):
        self.bot.start_webhook()
