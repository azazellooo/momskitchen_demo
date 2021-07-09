from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from accounts.models import Organization
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser

class PositionListViewTests(TestCase):
    fixtures = ['positions_test_data.json']
    response = None

    def setUp(self):
        self.factory = RequestFactory()

        self.organization = Organization.objects.create(**{
            'name': 'Attractor'
        })
        self.tg_user = TelegramUser.objects.create(**{
            'telegram_id': '1455413201',
            'first_name': 'Begaiym',
            'username': 'monpassan'
        })
        self.web_user = Employe.objects.create(**{
            'tg_user': self.tg_user,
            'organization_id': self.organization,
            'username': 'Gosha'
        })
        self.user_token = UserToken.objects.create(**{
            'user': self.web_user
        })
        kwargs = {'token': self.user_token.key}
        url = reverse('profile', kwargs=kwargs)
        self.request = Client()
        self.response = self.request.get(url)
        self.response = self.request.get(reverse('kitchen:list_position'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_positions_response(self):
        if len(self.response.context['dishes']) <= 0:
            self.assertContains(self.response, 'Нет блюд')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'd'
        search_response = self.request.get('/kitchen/position/list/', {'search_value': search_field_inner})
        print(search_response.context)
        [self.assertIn(search_field_inner, dish.name) for dish in search_response.context['dishes']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['dishes']), 5)
