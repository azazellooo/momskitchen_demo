import json
from time import sleep
import requests
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser
from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome

from KitchenWeb.models import Offering
from KitchenWeb.views.offering import OfferingCreateView
from accounts.models import Organization


class OfferingCreateViewTests(TestCase):

    def setUp(self):

        self.data = {
            "position": 123,
            "garnish": "1",
            "additional": '100',
            "supplement": 'asd',
            "date": '2021-07-06'
        }
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
        self.request = RequestFactory().post(reverse("kitchen:offering_create"), data=self.data)
        self.response = OfferingCreateView.as_view()(self.request)

    def test_proper_template(self):
        self.assertTemplateUsed("offering/create.html")

    def test_get_request_returns_200(self):

        # get request means request by method "GET"

        response = self.client.get(reverse("kitchen:offering_create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/offering/create/', self.request.path)


class OfferingListViewTests(TestCase):
    fixtures = ['offering_test_data.json']
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
        self.response = self.request.get(reverse('kitchen:offering_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_offerings_response(self):
        if len(self.response.context['offerings']) <= 0:
            self.assertContains(self.response, 'Нет предложений по позиции')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'd'
        search_response = self.request.get('/kitchen/offering/list', {'search_value': search_field_inner})
        print(search_response.context)
        [self.assertIn(search_field_inner, offering.position) for offering in search_response.context['offerings']]

    # def test_is_paginated_by_5(self):
    #     self.assertLessEqual(len(self.response.context['offerings']), 5)