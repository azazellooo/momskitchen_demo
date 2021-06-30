import json
from time import sleep
import requests

from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome

from KitchenWeb.models import Additional
from KitchenWeb.views import OrganizationCreateView
from KitchenWeb.views.additional import AdditionalCreateView
from accounts.models import Organization


class AdditionalListViewTests(TestCase):
    fixtures = ['additionals_test_data.json']
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('kitchen:additional_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_additional_response(self):
        if len(self.response.context['additionals']) <= 0:
            self.assertContains(self.response, 'Нет дополнений')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'd'
        search_response = self.client.get('/kitchen/additional/list/', {'search_value': search_field_inner})
        print(search_response.context)
        [self.assertIn(search_field_inner, additional.name) for additional in search_response.context['additionals']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['additionals']), 5)


class AdditionalCreateViewTest(TestCase):
    def setUp(self):
        x = '{"0.5": {"comment": "Comment", "pricing": "25"}}'
        self.data = {
            "name": "rice",
            "sampling_order": "12",
            "base_price": 1400,
            "extra_price": json.loads(x)
        }
        self.request = RequestFactory().post(reverse("kitchen:additional_create"), data=self.data)
        self.response = AdditionalCreateView.as_view()(self.request)
        self.factory = RequestFactory()
        self.garnish = Additional.objects.create(**self.data)

    def test_proper_template(self):
        self.assertTemplateUsed("additional/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:additional_create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/additional/create', self.request.path)

    def test_create(self):
        self.assertTrue(Additional.objects.filter(name='rice').exists())

    def test_field_values(self):
        self.assertEqual('rice', self.garnish.name)
        self.assertEqual('12', self.garnish.sampling_order)
        self.assertEqual(1400, self.garnish.base_price)
        self.assertEqual(json.loads('{"0.5": {"comment": "Comment", "pricing": "25"}}'), self.garnish.extra_price)