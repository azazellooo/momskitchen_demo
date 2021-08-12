import json
import time
from time import sleep
import requests
from django.contrib.sessions.middleware import SessionMiddleware
from webdriver_manager.chrome import ChromeDriverManager

from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, AdditionalFactory
from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome
from accounts.models import Employee, UserToken, Organization
from KitchenWeb.models import Additional
from KitchenWeb.views import OrganizationCreateView
from KitchenWeb.views.additional import AdditionalCreateView, AdditionalDetailUpdateView
from accounts.models import Organization
from mixer.backend.django import mixer


class AdditionalListViewTests(TestCase):
    fixtures = ['additionals_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:additional_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_additional_response(self):
        if len(self.response.context['additionals']) <= 0:
            self.assertContains(self.response, 'Нет еще такого дополнения')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'd'
        search_response = self.client.get('/kitchen/additional/list/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, additional.name) for additional in search_response.context['additionals']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['additionals']), 5)


class AdditionalCreateViewTest(TestCase):
    def setUp(self):
        x = '{"0.5": {"comment": "Comment", "pricing": "25"}}'
        self.data = {
            "name": "rice",
            "sampling_order": 12,
            "base_price": 1400,
            "extra_price": json.loads(x)
        }
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.request = RequestFactory().post(reverse("kitchen:additional_create"), data=self.data)
        self.middleware = SessionMiddleware()
        self.middleware.process_request(self.request)
        self.request.session.save()
        self.request.session['token'] = str(self.token.key)
        self.response = AdditionalCreateView.as_view()(self.request)
        self.factory = RequestFactory()
        self.additional = Additional.objects.create(**self.data)

    def test_proper_template(self):
        self.assertTemplateUsed("additional/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:additional_create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/additional/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Additional.objects.filter(name='rice').exists())

    def test_field_values(self):
        self.assertEqual('rice', self.additional.name)
        self.assertEqual(12, self.additional.sampling_order)
        self.assertEqual(1400, self.additional.base_price)
        self.assertEqual(json.loads('{"0.5": {"comment": "Comment", "pricing": "25"}}'), self.additional.extra_price)


class AdditionalDetailUpdateViewTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.additional = AdditionalFactory()

    def test_proper_template(self):
        self.assertTemplateUsed("additional/detail_update.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:additional_detail_update", kwargs={'pk': self.additional.pk}))
        self.assertEqual(200, response.status_code)

    def test_update_additional(self):
        self.data_to_update = {
            'name': 'another test ',
            'sampling_order': 3,
            'base_price': 432,
            'extra_price': AdditionalFactory.create().extra_price
        }
        self.response = self.client.post(reverse('kitchen:additional_detail_update', kwargs={'pk': self.additional.pk}),
                                    data=self.data_to_update)
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, reverse("kitchen:additional_list"))
        self.additional.refresh_from_db()
        self.assertEqual('another test ', self.additional.name)
        self.assertEqual(3, self.additional.sampling_order)
        self.assertEqual(432, self.additional.base_price)

