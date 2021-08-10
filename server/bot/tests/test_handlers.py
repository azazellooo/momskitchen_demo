from bot.handlers.main_commands import MainCommandsHandler
from bot.tests.base_telegrambot import BaseBot
from messages.bot_messages import *
from accounts.models import Employee, UserToken
from KitchenWeb.tests.factory_boy import EmployeeFactory, UserTokenFactory

class TestMainCommandsHandler(BaseBot):

    my_invalid_link = '/start 2887dff6-7ef5-4071-af5c-6b3e50f833ab'

    my_handler = MainCommandsHandler

    def setUp(self):
        super(TestMainCommandsHandler, self).setUp()

    def send_bot_message(self, user_telegram_chat_id, message):
        update, context = self.get_context_and_update(
            username='qwe',
            message=message,
            user_id=user_telegram_chat_id,
            chat_id=user_telegram_chat_id
        )
        return update, context

    def test_command_start_not_deep_link_real_user(self):
        update, context = self.send_bot_message(self.my_user.tg_id, '/start')
        telegram = self.get_telegram_instance()
        telegram.start(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), BOT_ALREADY_STARTED)

    def test_command_start_not_deep_link_not_user(self):
        update, context = self.send_bot_message('45678', '/start')
        telegram = self.get_telegram_instance()
        telegram.start(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), USER_NOT_FOUND)

    def test_command_start_invalid_link(self):
        update, context = self.send_bot_message(self.my_user.tg_id, self.my_invalid_link)
        telegram = self.get_telegram_instance()
        telegram.start(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), INVALID_LINK)

    def test_command_start_user_already_signed_up(self):
        EmployeeFactory(tg_username='qwe', tg_id=self.my_user.tg_id, organization_id=self.my_organization)
        update, context = self.send_bot_message(self.my_user.tg_id, self.my_deep_link)
        telegram = self.get_telegram_instance()
        telegram.start(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), USER_ALREADY_SIGNED_UP)

    def test_command_start_real_user(self):
        update, context = self.send_bot_message(self.my_user.tg_id, self.my_deep_link)
        telegram = self.get_telegram_instance()
        telegram.start(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), WELCOME[0]+'qwe'+WELCOME[1])
        self.assertTrue(telegram.bot.send_message.call_args.reply_markup is not None)

    def test_command_start_nextstep(self):
        update, context = self.send_bot_message(self.my_user.tg_id, 'lola')
        telegram = self.get_telegram_instance()
        telegram.nextstep(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), DATA_SAVED)
        self.assertTrue(Employee.objects.filter(tg_username=self.my_user.tg_username, username='lola').exists())

    def test_command_stop_not_real_user(self):
        update, context = self.send_bot_message('2345676789', '/stop')
        telegram = self.get_telegram_instance()
        telegram.stop(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), USER_NOT_FOUND)

    def test_command_stop_real_user_active(self):
        update, context = self.send_bot_message(self.my_user.tg_id, '/stop')
        telegram = self.get_telegram_instance()
        telegram.stop(update, context)
        self.assertTrue(Employee.objects.filter(tg_username=self.my_user.tg_username, is_active=False).exists())
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), MAILING_OFF)

    def test_command_stop_real_user_inactive(self):
        my_user = EmployeeFactory(tg_username='qwe', tg_id='123', is_active=False, organization_id=self.my_organization)
        update, context = self.send_bot_message(my_user.tg_id, '/stop')
        telegram = self.get_telegram_instance()
        telegram.stop(update, context)
        self.assertTrue(Employee.objects.filter(tg_username=my_user.tg_username, is_active=False).exists())
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), MAILING_ALREADY_OFF)

    def test_command_restart_not_real_user(self):
        update, context = self.send_bot_message('2345679', '/restart')
        telegram = self.get_telegram_instance()
        telegram.restart(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), USER_NOT_FOUND)

    def test_command_restart_real_user_inactive(self):
        my_user = EmployeeFactory(tg_username='qwe', tg_id='123', is_active=False, organization_id=self.my_organization)
        update, context = self.send_bot_message(my_user.tg_id, '/restart')
        telegram = self.get_telegram_instance()
        telegram.restart(update, context)
        self.assertTrue(Employee.objects.filter(tg_username=my_user.tg_username, is_active=True).exists())
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), WELCOME_BACK[0]+my_user.tg_username+WELCOME_BACK[1])

    def test_command_restart_real_user_active(self):
        my_user = EmployeeFactory(tg_username='qwe', tg_id='123', is_active=True, organization_id=self.my_organization)
        update, context = self.send_bot_message(my_user.tg_id, '/restart')
        telegram = self.get_telegram_instance()
        telegram.restart(update, context)
        self.assertTrue(Employee.objects.filter(tg_username=my_user.tg_username, is_active=True).exists())
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), ALREADY_ACTIVE)

    def test_command_login_not_real_user(self):
        update, context = self.send_bot_message('456654', '/login')
        telegram = self.get_telegram_instance()
        telegram.login(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), CANNOT_GIVE_TOKEN)

    def test_command_login_real_user_without_token(self):
        update, context = self.send_bot_message(self.my_user.tg_id, '/login')
        telegram = self.get_telegram_instance()
        telegram.login(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), GIVE_TOKEN+str((UserToken.objects.get(user=self.my_user)).key))

    def test_command_login_real_user_with_token(self):
        UserTokenFactory(user=self.my_user)
        update, context = self.send_bot_message(self.my_user.tg_id, '/login')
        telegram = self.get_telegram_instance()
        telegram.login(update, context)
        self.assertTrue(telegram.bot.send_message.called)
        args, message = telegram.bot.send_message.call_args
        self.assertEqual(message.get('text'), TOKEN_ALREADY_GIVEN)
        self.assertTrue(UserToken.objects.filter(user=self.my_user).exists())














