from django.test import TestCase
from django.urls import reverse
from KitchenWeb.tests.factory_boy import CategoryFacroty



class CategoryListViewTest(TestCase):
    fixtures =['category_test_data.json']
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('kitchen:category_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_category_response(self):
        if len(self.response.context['categories']) <= 0:
            self.assertContains(self.response, 'Категории нет.')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'jam'
        search_response = self.client.get('/kitchen/categories/list/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, category.category_name) for category in search_response.context['categories']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['categories']), 5)