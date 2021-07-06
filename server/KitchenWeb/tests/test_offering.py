import json
from time import sleep
import requests

from django.test import TestCase, RequestFactory, LiveServerTestCase
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
        self.request = RequestFactory().post(reverse("kitchen:offering_create"), data=self.data)
        self.response = OfferingCreateView.as_view()(self.request)

    def test_proper_template(self):
        self.assertTemplateUsed("offering/create.html")

    def test_get_request_returns_200(self):

        # get request means request by method "GET"

        response = self.client.get(reverse("kitchen:offering_create"))
        self.assertEqual(response.status_code, 401)

    def test_proper_path(self):
        self.assertEqual('/kitchen/offering/create/', self.request.path)

    # def test_create(self):
    #     self.assertTrue(Offering.objects.filter(date=2021-07-06).exists())

    # def test_field_values(self):
    #     self.assertEqual('123', self.offering.position)
    #     self.assertEqual('1', self.offering.garnish)
    #     self.assertEqual('100', self.offering.additional)
    #     self.assertEqual('asd', self.offering.supplement)
    #     self.assertEqual('2021-07-06', self.offering.date)




# class OfferingCreateViewTests(TestCase):
#
#     data = {
#         "position": "123",
#         "garnish": "1",
#         "additional": '100',
#         "supplement": 'asd',
#         "date": '2021-07-06'
#     }
#     request = RequestFactory().post(reverse("kitchen:offering_create"), data=data)
#     response = OfferingCreateViewTests.as_view()(request)
#
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.organization = Organization.objects.create(**self.data)
#
#     def test_proper_template(self):
#         self.assertTemplateUsed("organizations/create.html")
#
#     def test_get_request_returns_200(self):
#
#         # get request means request by method "GET"
#
#         response = self.client.get(reverse("kitchen:offering_create"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_proper_path(self):
#         self.assertEqual('/offering/create/', self.request.path)
#
#     def test_create(self):
#         self.assertTrue(Organization.objects.filter(name='Test Organization').exists())
#
#     def test_post(self):
#         self.assertEqual(self.response.status_code, 200)
#         self.assertContains(self.response, 'Test Organization')
#
#     def test_field_values(self):
#         self.assertEqual(self.organization.position)
#         self.assertEqual(self.organization.garnish)
#         self.assertFalse(self.organization.additional)
#         self.assertTrue(self.organization.supplement)
#         self.assertTrue(self.organization.date)