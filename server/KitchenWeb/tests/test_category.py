from time import sleep
import requests
from django.contrib.sessions.middleware import SessionMiddleware

from accounts.models import Employe, UserToken, Organization
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, TelegramUserFactory
from kitchen5bot.models import TelegramUser
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from KitchenWeb.views.category import CategoryCreateView
from KitchenWeb.models import Category
import random
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class CategoryListViewTest(TestCase):
    fixtures = ['category_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.telegram_user = TelegramUserFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, tg_user=self.telegram_user)
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


# class CategoryCreateViewTest(TestCase):
#
#     def setUp(self):
#         # self.client.get(reverse('profile', kwargs={'token': self.token.key}))
#         self.category = Category.objects.create(**self.data)
#
#         # request.session['token'] = str(self.token.key)
#
#     data = {
#         "category_name": "Test Category",
#         "order": 6
#     }
#     organization = OrganizationFactory()
#     telegram_user = TelegramUserFactory()
#     employee = EmployeeFactory(organization_id=organization, tg_user=telegram_user)
#     token = UserTokenFactory(user=employee)
#     request = RequestFactory().post(reverse("kitchen:category_create"), data=data)
#     middleware = SessionMiddleware()
#     middleware.process_request(request)
#     request.session.save()
#     request.session['token'] = token.key
#     response = CategoryCreateView.as_view()(request)
#
#     def test_proper_template(self):
#         self.assertTemplateUsed("category/create.html")
#
#     def test_get_request_returns_200(self):
#         response = self.client.get(reverse("kitchen:category_list"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_proper_path(self):
#         self.assertEqual('/kitchen/categories/create/', self.request.path)
#
#     def test_create(self):
#         self.assertTrue(Category.objects.filter(category_name='Test Category').exists())
#         self.assertTrue(Category.objects.filter(order=6).exists())
#
#     def test_post(self):
#         self.assertEqual(302, self.response.status_code)
#
#     def test_field_values(self):
#         self.assertEqual(self.category.category_name, 'Test Category')
#         self.assertEqual(self.category.order, 6)


# class OrganizationDetailUpdateViewTests(StaticLiveServerTestCase):
#
#     def setUp(self):
#         self.o = Category.objects.create(**{
#         'category_name': 'test category ',
#         'order': '6'
#         })
#         self.driver = webdriver.Chrome(ChromeDriverManager().install())
#         self.driver.maximize_window()
#         self.organization = OrganizationFactory()
#         self.employee = EmployeeFactory(organization_id=self.organization)
#         self.token = UserTokenFactory(user=self.employee)
#         self.driver.get(f'{self.live_server_url}/accounts/{self.token.key}/')
#
#     def tearDown(self):
#         self.o.delete()
#         self.driver.close()
#
#     def test_update_organization(self):
#         self.driver.get(url=f'{self.live_server_url}/kitchen/category/update/detail/{self.o.pk}/')
#         self.driver.find_element_by_id('edit_btn').click()
#         self.driver.find_element_by_name('category_name').clear()
#         self.driver.find_element_by_name('category_name').send_keys('test updated category_name')
#         self.driver.find_element_by_name('order').clear()
#         self.driver.find_element_by_name('order').send_keys('9')
#         self.driver.find_element_by_id('submit').click()
#         self.o.refresh_from_db()
#         self.assertEqual(f'{self.live_server_url}/kitchen/categories/list/', self.driver.current_url)
#         self.assertEqual('test updated category_name', self.o.category_name)
#         self.assertEqual(9, self.o.order)
#
#
#     def test_form_disabled_enabled(self):
#         self.driver.get(url=f'{self.live_server_url}/kitchen/category/update/detail/{self.o.pk}/')
#         inputs = self.driver.find_elements_by_tag_name('input')
#         category_name = self.driver.find_element_by_id('id_category_name')
#         self.assertFalse(inputs[0].is_enabled())
#         self.assertFalse(category_name.is_enabled())
#         self.driver.find_element_by_id('edit_btn').click()
#         self.assertTrue(inputs[0].is_enabled())
#         self.assertTrue(category_name.is_enabled())
#         self.driver.find_element_by_id('cancel_btn').click()
#         self.assertFalse(inputs[0].is_enabled())
#         self.assertFalse(category_name.is_enabled())
