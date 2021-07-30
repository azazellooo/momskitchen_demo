from datetime import datetime
from django.test import TransactionTestCase
from unittest.mock import Mock
from telegram import (
    Bot, Chat, Message, User, Update
)
from telegram.ext import CallbackContext, Dispatcher, Updater
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory


class BaseBot(TransactionTestCase):

    my_handler = None

    def setUp(self):
        self.my_organization = OrganizationFactory()
        self.my_deep_link = '/start ' + str(self.my_organization.secondary_key)
        self.my_user = EmployeeFactory()

    @staticmethod
    def get_update(username, message, user_id, chat_id, chat_type):
        user = User(user_id, "qwe", is_bot=False)
        chat = Chat(id=chat_id, username=username, type=chat_type)
        message = Message(1, datetime.now(), chat, user, text=message)
        return Update(1, message=message)

    def get_context_and_update(self, username='qwe', message='123', user_id=1234, chat_id=890,chat_type='qwerty'):
        context = Mock(spec=CallbackContext)
        update = self.get_update(username, message, user_id, chat_id, chat_type)
        return update, context

    def get_telegram_instance(self):
        my_dispatcher = Mock(spec=Dispatcher)
        my_telegram = self.my_handler(my_dispatcher)
        my_telegram.bot = Mock(spec=Bot)
        return my_telegram


