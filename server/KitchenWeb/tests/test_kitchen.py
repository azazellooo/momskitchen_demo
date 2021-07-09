from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser
from KitchenWeb.models import Supplement


class SupplementListViewTests(TestCase):
    fixtures = ['supplements_test_data.json']
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
        self.response = self.request.get(reverse('kitchen:supplement-list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_supplements_response(self):
        if len(self.response.context['supplements']) <= 0:
            self.assertContains(self.response, 'Надбавок нет.')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'jam'
        search_response = self.request.get('/kitchen/supplements/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, supplement.name) for supplement in search_response.context['supplements']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['supplements']), 5)


class SupplementUpdateTest(TestCase):
    def test_update_supplement(self):
        self.supplement = Supplement.objects.create(name='Гречка', price=130)
        self.supplement.save()
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
        self.client = Client()
        self.response = self.client.get(url)
        response = self.client.post(
            reverse('kitchen:detail_update_supplement', kwargs={'pk': self.supplement.id}),
            {'name': 'Рис', 'price': '131'}
        )
        self.assertEqual(response.status_code, 302)
        self.supplement.refresh_from_db()
        self.assertEqual('Рис', self.supplement.name)
