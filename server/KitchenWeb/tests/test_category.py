from django.test import TestCase, RequestFactory
from django.urls import reverse
from KitchenWeb.views.category import CategoryCreateView
from KitchenWeb.models import Category


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


class CategoryCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(**self.data)

    data = {
        "category_name": "Test Category",
        "order": 5
    }

    request = RequestFactory().post(reverse("kitchen:category_create"), data=data)
    response = CategoryCreateView.as_view()(request)


    def test_proper_template(self):
        self.assertTemplateUsed("category/create.html")

    def test_get_request_returns_200(self):

        # get request means request by method "GET"

        response = self.client.get(reverse("kitchen:category_list"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/categories/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Category.objects.filter(category_name='Test Category').exists())
        self.assertTrue(Category.objects.filter(order=5).exists())

    def test_post(self):
        self.assertEqual(302, self.response.status_code)

    def test_field_values(self):
        self.assertEqual(self.category.category_name, 'Test Category')
        self.assertEqual(self.category.order, 5)