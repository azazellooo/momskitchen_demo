# import datetime
# import json
# import time
# from time import sleep
# import requests
# from django.contrib.sessions.middleware import SessionMiddleware
#
# from accounts.models import Employe, UserToken, Organization
# from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.urls import reverse
# from selenium.webdriver import Chrome
# from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, DishFactory, \
#     GarnishFactory, SupplementFactory, AdditionalFactory, OfferingFactory
# from KitchenWeb.models import Offering
# from KitchenWeb.views.offering import OfferingCreateView
# from accounts.models import Organization
#
#
# class OfferingCreateViewTests(TestCase):
#
#     def setUp(self):
#         self.data = {
#             "position": 123,
#             "garnish": "1",
#             "additional": '100',
#             "supplement": 'asd',
#             "date": '2021-07-06'
#         }
#         self.organization = OrganizationFactory()
#         self.employee = EmployeeFactory(organization_id=self.organization)
#         self.token = UserTokenFactory(user=self.employee)
#         self.client.get(reverse('profile', kwargs={'token': self.token.key}))
#         self.request = RequestFactory().post(reverse("kitchen:offering_create"), data=self.data)
#         self.middleware = SessionMiddleware()
#         self.middleware.process_request(self.request)
#         self.request.session.save()
#         self.request.session['token'] = self.token.key
#         self.response = OfferingCreateView.as_view()(self.request)
#
#     def test_proper_template(self):
#         self.assertTemplateUsed("offering/create.html")
#
#     def test_get_request_returns_200(self):
#         response = self.client.get(reverse("kitchen:offering_create"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_proper_path(self):
#         self.assertEqual('/kitchen/offering/create/', self.request.path)
#
#
# class OfferingListViewTests(TestCase):
#     fixtures = ['offering_test_data.json']
#     response = None
#
#     def setUp(self):
#         self.organization = OrganizationFactory()
#         self.employee = EmployeeFactory(organization_id=self.organization)
#         self.token = UserTokenFactory(user=self.employee)
#         self.client.get(reverse('profile', kwargs={'token': self.token.key}))
#         self.response = self.client.get(reverse('kitchen:offering_list'))
#
#     def test_status_code_200(self):
#         self.assertEqual(self.response.status_code, 200)
#
#     def test_is_paginated_by_5(self):
#         self.assertGreaterEqual(5, len(self.response.context['offerings']))
#
#     def test_no_offerings_response(self):
#         if len(self.response.context['offerings']) <= 0:
#             self.assertContains(self.response, 'Нет ещё такого предложения ')
#
#     def test_valid_response_for_search_query(self):
#         search_field_inner = 'd'
#         search_response = self.client.get('/kitchen/offering/list', {'search_value': search_field_inner})
#         [self.assertIn(search_field_inner, offering.position) for offering in search_response.context['offerings']]
#
#
# class OfferingDetailUpdateViewTests(TestCase):
#
#     def setUp(self):
#         self.organization = OrganizationFactory()
#         self.employee = EmployeeFactory(organization_id=self.organization)
#         self.token = UserTokenFactory(user=self.employee)
#         self.client.get(reverse('profile', kwargs={'token': self.token.key}))
#         self.position = DishFactory()
#         garnish = GarnishFactory()
#         supplement = SupplementFactory()
#         additional = AdditionalFactory()
#         self.offering = OfferingFactory(position=self.position, garnish=garnish, supplement=supplement,
#                                         additional=additional)
#         self.response = self.client.get(reverse('kitchen:offering-detail', kwargs={'pk': self.offering.pk}))
#
#     def test_status_200(self):
#         self.assertEqual(200, self.response.status_code)
#
#     def test_update_offering(self):
#         data_to_update = {
#             'position': DishFactory(name='another test dish').pk,
#             'garnish': GarnishFactory(name='another test garnish').pk,
#             'supplement': SupplementFactory(name='another test supplement').pk,
#             'additional': AdditionalFactory(name='another test additional').pk,
#             'qty_portion': 6,
#             'date': '2021-07-15'
#         }
#
#         response = self.client.post(reverse('kitchen:offering-detail', kwargs={'pk': self.offering.pk}), data=data_to_update)
#         self.assertEqual(302, response.status_code)
#         self.assertRedirects(response, reverse('kitchen:offering_list'))
#         self.offering.refresh_from_db()
#         self.assertEqual('another test dish', self.offering.position.name)
#         self.assertEqual('another test garnish', self.offering.garnish.name)
#         self.assertEqual('another test supplement', self.offering.supplement.name)
#         self.assertEqual('another test additional', self.offering.additional.name)
#         self.assertEqual(6, self.offering.qty_portion)
#         self.assertEqual(datetime.date(2021, 7, 15), self.offering.date)
