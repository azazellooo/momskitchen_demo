from django.test import TestCase
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, BalanceChangeFactory, \
    TelegramChatFactory, TelegramStateFactory, TelegramUserFactory


class NotificationAfterTransactionTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.tg_user = TelegramUserFactory(telegram_id=941151624)
        self.employee = EmployeeFactory(organization_id=self.organization, tg_user=self.tg_user)
        self.tg_chat = TelegramChatFactory(telegram_id=self.employee.tg_user.telegram_id)
        self.state = TelegramStateFactory(telegram_chat=self.tg_chat, telegram_user=self.employee.tg_user)
        self.transaction = BalanceChangeFactory(employe=self.employee)

    def test_proper_message(self):
        if self.transaction.type == 'accrual':
            self.assertEqual(f'на ваш баланс было начислено '
                             f'{self.transaction.sum_balance} сомов. Ваш текущий баланс: '
                             f'{self.transaction.employe.total_balance + self.transaction.sum_balance} '
                             f'сомов.Комментарий к транзакции: {self.transaction.comment}',
                             self.transaction.notification_text)

