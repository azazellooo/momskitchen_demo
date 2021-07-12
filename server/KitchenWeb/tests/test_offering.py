import json
import time
from time import sleep
import requests
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser
from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory
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
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.request = RequestFactory().post(reverse("kitchen:offering_create"), data=self.data)
        self.response = OfferingCreateView.as_view()(self.request)

    def test_proper_template(self):
        self.assertTemplateUsed("offering/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:offering_create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/offering/create/', self.request.path)


class OfferingListViewTests(TestCase):
    fixtures = ['offering_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:offering_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    # def test_no_offerings_response(self):
    #     if len(self.response.context['offerings']) <= 0:
    #         self.assertContains(self.response, 'Нет ещё такого предложения ')

    # def test_valid_response_for_search_query(self):
    #     search_field_inner = 'd'
    #     search_response = self.client.get('/kitchen/offering/list', {'search_value': search_field_inner})
    #     [self.assertIn(search_field_inner, offering.position) for offering in search_response.context['offerings']]
