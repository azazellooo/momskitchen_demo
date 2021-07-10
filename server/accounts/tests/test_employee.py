import itertools

import factory
from django.test import TestCase
from django.urls import reverse

from KitchenWeb.tests.factory_boy import BalanceChangeFactory, EmployeeFactory, UserTokenFactory
from accounts.models import UserToken


class EmployeeTransactionHistoryViewTests(TestCase):

    def setUp(self):
        self.employee = EmployeeFactory()
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.transactions = [BalanceChangeFactory(employe=self.employee, sum_balance=i, comment=f'comment {i}') for i in range(5)]
        self.response = self.client.get(reverse('employee-transactions', kwargs={'pk': self.employee.pk}))
        self.session = self.client.session
        self.session['token'] = self.token.key

    def test_user_authenticated(self):
        self.assertNotEqual(None, self.session.get('token', None))
        self.assertTrue(UserToken.objects.filter(key=self.session.get('token')).exists())

    def test_is_admin(self):
        self.assertTrue(self.employee.is_admin)

    def test_proper_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/transaction_history.html')

    def test_status_200(self):
        self.assertEqual(200, self.response.status_code)

    def test_no_transactions(self):
        if self.employee.bal_em.count() < 1:
            self.assertContains(self.response, 'Нет транзакций')

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['object_list']), 5)

# Create your tests here.
