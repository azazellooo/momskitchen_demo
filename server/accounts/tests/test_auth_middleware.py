from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, RequestFactory
import requests
from accounts.models import Organization, Employee
from kitchen5bot.models import TelegramUser
from accounts.views import *



class CustomAuthMiddlewareTests(StaticLiveServerTestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.organization = Organization.objects.create(**{
            'name': 'Attractor'
        })
        # self.tg_user = TelegramUser.objects.create(**{
        #     'telegram_id': '1455413201',
        #     'first_name': 'Begaiym',
        #     'username': 'monpassan'
        # })
        self.web_user = Employee.objects.create(**{
            'tg_username': 'qwe',
            'tg_id': 123,
            'organization_id': self.organization,
            'username': 'Gosha'
        })
        self.user_token = UserToken.objects.create(**{
            'user': self.web_user
        })


    def test_browse_unauthenticated(self):
        response = requests.get(url=f'{self.live_server_url}/organizations/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/organizations/create/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/organizations/{self.organization.pk}/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/kitchen/supplements/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/kitchen/supplements/create/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/kitchen/position/list/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/kitchen/position/create/')
        self.assertEqual(401, response.status_code)
        response = requests.get(url=f'{self.live_server_url}/kitchen/categories/create/')
        self.assertEqual(401, response.status_code)


    def test_login_without_token(self):
        request = self.factory.get('profile.html')
        self.assertRaises(KeyError)

    def test_login_with_token(self):
        kwargs = {'token': self.user_token.key}
        url = reverse('profile', kwargs=kwargs)
        request = Client()
        response = request.get(url)
        self.assertEqual(request.session['token'], str(self.user_token.key))
        self.assertEqual(response.status_code, 302)