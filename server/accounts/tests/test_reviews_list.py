import json
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory
from KitchenWeb.views import GarnishCreateView


class ReviewListViewTests(TestCase):
    fixtures = ['reviews_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('reviews_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_positions_response(self):
        if len(self.response.context['reviews']) <= 0:
            self.assertContains(self.response, 'Отзывов еще нет :(')

    def test_valid_response_for_search_query(self):
        search_field_inner = 't'
        search_response = self.client.get('/accounts/reviews/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, review.text_review) for review in search_response.context['reviews']]

