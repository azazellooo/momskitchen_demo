from time import sleep
import requests

from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome

from KitchenWeb.views import OrganizationCreateView
from accounts.models import Organization


class AdditionalListViewTests(TestCase):
    fixtures = ['additional_test_data.json']
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('kitchen:additional_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_organization_response(self):
        if len(self.response.context['additionals']) <= 0:
            self.assertContains(self.response, 'Нет организаций')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'a'
        search_response = self.client.get('/additional/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, organization.name) for organization in
         search_response.context['additionals']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['additional']), 5)