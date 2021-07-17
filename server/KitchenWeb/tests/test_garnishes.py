import json

from django.contrib.sessions.middleware import SessionMiddleware
from webdriver_manager.chrome import ChromeDriverManager

from KitchenWeb.views.category import CategoryCreateView
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.test.utils import override_settings
from selenium.webdriver import Chrome
from KitchenWeb.models import Garnish
from KitchenWeb.views import GarnishCreateView


class GarnishListViewTests(TestCase):
    fixtures = ['garnishes_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
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
        self.assertGreaterEqual(5, len(self.response.context['garnishes']))


class GarnishCreateViewTests(TestCase):

    def setUp(self):
        x = '{"0.5": {"comment": "Comment", "pricing": "25"}}'
        self.data = {
            "name": "garnish",
            "order": "1",
            "base_price": 100,
            "extra_price": json.loads(x)
        }
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.request = RequestFactory().post(reverse("kitchen:create_garnish"), data=self.data)
        self.middleware = SessionMiddleware()
        self.middleware.process_request(self.request)
        self.request.session.save()
        self.request.session['token'] = self.token.key
        self.response = GarnishCreateView.as_view()(self.request)
        self.factory = RequestFactory()
        self.garnish = Garnish.objects.create(**self.data)

    def test_proper_template(self):
        self.assertTemplateUsed("garnishes/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:create_garnish"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/garnish/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Garnish.objects.filter(name='garnish').exists())

    def test_field_values(self):
        self.assertEqual('garnish', self.garnish.name)
        self.assertEqual('1', self.garnish.order)
        self.assertEqual(100, self.garnish.base_price)
        self.assertEqual(json.loads('{"0.5": {"comment": "Comment", "pricing": "25"}}'), self.garnish.extra_price)


# @override_settings(DEBUG=True)
# class GarnishDetailUpdateViewTests(StaticLiveServerTestCase):
#     def setUp(self):
#         json_field = "{\"0.3\": {\"comment\": \"Comment3\", \"pricing\": \"20\"}, \"0.5\": {\"comment\": \"Comment22222\", \"pricing\": \"20\"}}"
#         self.garnish = Garnish.objects.create(**{
#             "name": "test garnish",
#             "order": "1",
#             "base_price": 100,
#             "extra_price": json_field
#         })
#         self.driver = Chrome(ChromeDriverManager().install())
#         self.driver.maximize_window()
#         self.organization = OrganizationFactory()
#         self.employee = EmployeeFactory(organization_id=self.organization)
#         self.token = UserTokenFactory(user=self.employee)
#         self.driver.get(f'{self.live_server_url}/accounts/{self.token.key}/')
#
#     def tearDown(self):
#         self.garnish.delete()
#         self.driver.close()
#
#     def test_use_proper_html(self):
#         response = self.driver.get(f'{self.live_server_url}/kitchen/garnish/{self.garnish.pk}/')
#         self.assertTemplateUsed(response, 'garnishes/detail_update.html')
#
#     def test_disabled_enabled_fields(self):
#         self.driver.get(url=f'{self.live_server_url}/kitchen/garnish/{self.garnish.pk}/')
#         inputs = self.driver.find_elements_by_tag_name('input')
#         selects = self.driver.find_elements_by_tag_name('select')
#         buttons = self.driver.find_elements_by_class_name('plus-min-btn')
#         checking_elems = [y for x in [inputs, selects, buttons] for y in x]
#         edit_btn = self.driver.find_element_by_id('edit_btn')
#         cancel_btn = self.driver.find_element_by_id('cancel_btn')
#         self.assertTrue(edit_btn.is_displayed())
#         self.assertFalse(cancel_btn.is_displayed())
#         for i in checking_elems:
#             self.assertFalse(i.is_enabled())
#         edit_btn.click()
#         self.assertTrue(cancel_btn.is_displayed())
#         self.assertFalse(edit_btn.is_displayed())
#         for i in checking_elems:
#             self.assertTrue(i.is_enabled())
#         cancel_btn.click()
#         for i in checking_elems:
#             self.assertFalse(i.is_enabled())
#
#     def test_update(self):
#         self.driver.get(url=f'{self.live_server_url}/kitchen/garnish/{self.garnish.pk}/')
#         self.driver.find_element_by_id('edit_btn').click()
#         self.driver.find_element_by_name('name').clear()
#         self.driver.find_element_by_name('name').send_keys('updated garnish name')
#         self.driver.find_element_by_name('order').clear()
#         self.driver.find_element_by_name('order').send_keys('3')
#         self.driver.find_element_by_id('comment1').clear()
#         self.driver.find_element_by_name('comment1').send_keys('updated comment 1')
#         self.driver.find_element_by_id('pricing1').clear()
#         self.driver.find_element_by_name('pricing1').send_keys('123')
#         self.driver.find_element_by_id('comment2').clear()
#         self.driver.find_element_by_name('comment2').send_keys('updated comment 2')
#         self.driver.find_element_by_id('pricing2').clear()
#         self.driver.find_element_by_name('pricing2').send_keys('123')
#         self.driver.find_element_by_id('savePosition').click()
#         self.garnish.refresh_from_db()
#         self.assertEqual('updated garnish name', self.garnish.name)
#         self.assertEqual(3, self.garnish.order)
#         extra_dict = json.loads(self.garnish.extra_price)
#         self.assertEqual('updated comment 1', extra_dict['0.3']['comment'])
#         self.assertEqual('updated comment 2', extra_dict['0.5']['comment'])
#         self.assertEqual('123', extra_dict['0.3']['pricing'])
#         self.assertEqual('123', extra_dict['0.5']['pricing'])
#         self.assertEqual(f'{self.live_server_url}/kitchen/garnish/list/', self.driver.current_url)
#
#
#     def test_delete_extra_price(self):
#         self.driver.get(url=f'{self.live_server_url}/kitchen/garnish/{self.garnish.pk}/')
#         self.driver.find_element_by_id('edit_btn').click()
#         self.driver.find_elements_by_xpath("//button[@onclick='removeExtraBtn2(event);']")[0].click()
#         self.driver.find_element_by_id('savePosition').click()
#         self.garnish.refresh_from_db()
#         self.assertFalse('0.3' in self.garnish.extra_price)
