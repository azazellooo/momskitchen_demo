from django.test import TestCase
from django.urls import reverse
from accounts.models import Organization


class OrganizationsListViewTests(TestCase):
    fixtures = ['organizations_test_data.json']
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('kitchen:organization-list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_organization_response(self):
        if len(self.response.context['organizations']) <= 0:
            self.assertContains(self.response, 'Нет организаций')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'a'
        search_response = self.client.get('/organizations/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, organization.name) for organization in
         search_response.context['organizations']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['organizations']), 5)

