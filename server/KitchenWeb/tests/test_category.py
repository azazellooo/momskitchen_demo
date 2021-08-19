from django.contrib.sessions.middleware import SessionMiddleware
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, CategoryFactory
from django.test import TestCase, RequestFactory
from django.urls import reverse
from KitchenWeb.views.category import CategoryCreateView
from KitchenWeb.models import Category


class CategoryListViewTest(TestCase):
    fixtures = ['category_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
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
        self.data = {
            "category_name": "Test Category",
            "order": 6
        }
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.request = RequestFactory().post(reverse("kitchen:category_create"), data=self.data)
        self.middleware = SessionMiddleware()
        self.middleware.process_request(self.request)
        self.request.session.save()
        self.request.session['token'] = self.token.key
        self.response = CategoryCreateView.as_view()(self.request)
        self.factory = RequestFactory()
        self.category = Category.objects.create(**self.data)

    def test_proper_template(self):
        self.assertTemplateUsed("category/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:category_create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/categories/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Category.objects.filter(category_name='Test Category').exists())
        self.assertTrue(Category.objects.filter(order=6).exists())

    def test_post(self):
        self.assertEqual(302, self.response.status_code)

    def test_field_values(self):
        self.assertEqual("Test Category", self.category.category_name)
        self.assertEqual(6, self.category.order,)


class CategoryDetailUpdateViewTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.category = CategoryFactory()

    def test_proper_template(self):
        self.assertTemplateUsed("organizations/detail_update.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:category_update_detail", kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_category(self):

        data = {
            "category_name": "Test Category",
            "order": 6
        }
        response = self.client.post(reverse('kitchen:category_update_detail', kwargs={'pk': self.category.pk}),
                                    data=data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('kitchen:category_list'))
        self.category.refresh_from_db()
        self.assertEqual("Test Category", self.category.category_name)
        self.assertEqual(6, self.category.order)

