from django.core.management.base import BaseCommand
from bot.init_bot import BotInit


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot = BotInit()
        bot.launch()
