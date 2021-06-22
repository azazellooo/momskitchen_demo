from django.test import TestCase
from django.urls import reverse
from accounts.models import Organization


class PositionListViewTests(TestCase):
    fixtures = ['garnishes_test_data.json']
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('kitchen:list_garnish'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_positions_response(self):
        if len(self.response.context['garnishes']) <= 0:
            self.assertContains(self.response, 'Нет гарниров')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'd'
        search_response = self.client.get('/kitchen/garnish/list/', {'search_value': search_field_inner})
        print(search_response.context)
        [self.assertIn(search_field_inner, dish.name) for dish in search_response.context['garnishes']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['garnishes']), 5)

