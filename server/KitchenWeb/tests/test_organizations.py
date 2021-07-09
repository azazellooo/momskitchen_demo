from time import sleep
import requests
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser

from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome

from KitchenWeb.views import OrganizationCreateView
from accounts.models import Organization


class OrganizationsListViewTests(TestCase):
    fixtures = ['organizations_test_data.json']
    response = None

    def setUp(self):
        self.factory = RequestFactory()

        self.organization = Organization.objects.create(**{
            'name': 'Attractor'
        })
        self.tg_user = TelegramUser.objects.create(**{
            'telegram_id': '1455413201',
            'first_name': 'Begaiym',
            'username': 'monpassan'
        })
        self.web_user = Employe.objects.create(**{
            'tg_user': self.tg_user,
            'organization_id': self.organization,
            'username': 'Gosha'
        })
        self.user_token = UserToken.objects.create(**{
            'user': self.web_user
        })
        kwargs = {'token': self.user_token.key}
        url = reverse('profile', kwargs=kwargs)
        self.request = Client()
        self.response = self.request.get(url)
        self.response = self.request.get(reverse('kitchen:organization-list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_organization_response(self):
        if len(self.response.context['organizations']) <= 0:
            self.assertContains(self.response, 'Нет организаций')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'a'
        search_response = self.request.get('/organizations/', {'search_value': search_field_inner})
        [self.assertIn(search_field_inner, organization.name) for organization in
         search_response.context['organizations']]

    def test_is_paginated_by_5(self):
        self.assertLessEqual(len(self.response.context['organizations']), 5)


class OrganizationCreateViewTests(TestCase):
    data = {
        "name": "Test Organization",
        "payment": "('actual', 'фактический расчет')",
        "address": "Bishkek",
        "bonus_activation": False,
        "leave_review": True,
        "is_active": True
    }
    request = RequestFactory().post(reverse("kitchen:organization-create"), data=data)
    response = OrganizationCreateView.as_view()(request)

    def setUp(self):
        self.organization = Organization.objects.create(**{
            'name': 'Attractor'
        })
        self.tg_user = TelegramUser.objects.create(**{
            'telegram_id': '1455413201',
            'first_name': 'Begaiym',
            'username': 'monpassan'
        })
        self.web_user = Employe.objects.create(**{
            'tg_user': self.tg_user,
            'organization_id': self.organization,
            'username': 'Gosha'
        })
        self.user_token = UserToken.objects.create(**{
            'user': self.web_user
        })
        kwargs = {'token': self.user_token.key}
        url = reverse('profile', kwargs=kwargs)
        self.client = Client()
        self.response = self.client.get(url)
        self.factory = RequestFactory()
        self.organization = Organization.objects.create(**self.data)

    def test_proper_template(self):
        self.assertTemplateUsed("organizations/create.html")

    def test_get_request_returns_200(self):

        # get request means request by method "GET"

        response = self.client.get(reverse("kitchen:organization-create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/organizations/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Organization.objects.filter(name='Test Organization').exists())

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_field_values(self):
        self.assertEqual(self.organization.name, 'Test Organization')
        self.assertEqual(self.organization.address, 'Bishkek')
        self.assertFalse(self.organization.bonus_activation)
        self.assertTrue(self.organization.leave_review)
        self.assertTrue(self.organization.is_active)
        self.assertEqual(self.organization.payment, "('actual', 'фактический расчет')")


class OrganizationDetailUpdateViewTests(StaticLiveServerTestCase):

    def setUp(self):
        self.o = Organization.objects.create(**{
        "name": "Test Organization",
        "payment": "('actual', 'фактический расчет')",
        "address": "Bishkek",
        "bonus_activation": False,
        "leave_review": True,
        "is_active": True
        })
        self.driver = Chrome()
        self.driver.maximize_window()
    def tearDown(self):
        self.o.delete()
        self.driver.close()

    def test_update_organization(self):
        self.driver.get(url=f'{self.live_server_url}/organizations/{self.o.pk}')
        self.driver.find_element_by_id('edit_btn').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('test updated name')
        self.driver.find_element_by_name('leave_review').is_selected()
        self.driver.find_element_by_name('address').clear()
        self.driver.find_element_by_name('address').send_keys('Test updated address')
        self.driver.find_element_by_name('is_active').is_selected()
        self.driver.find_element_by_xpath("//select[@name='payment']/option[text()='накопительный расчет']")
        self.driver.find_element_by_name('bonus_activation').is_selected()
        self.driver.find_element_by_id('submit').click()
        self.o.refresh_from_db()
        self.assertEqual('test updated name', self.o.name)
        self.assertEqual('Test updated address', self.o.address)
        self.assertEqual(f'{self.live_server_url}/organizations/', self.driver.current_url)
        response = requests.get(self.driver.current_url)
        self.assertEqual(200, response.status_code)

    def test_form_disabled_enabled(self):
        self.driver.get(url=f'{self.live_server_url}/organizations/{self.o.pk}')
        inputs = self.driver.find_elements_by_tag_name('input')
        self.assertFalse(inputs[0].is_enabled())
        self.driver.find_element_by_id('edit_btn').click()
        self.assertTrue(inputs[0].is_enabled())
        self.driver.find_element_by_id('cancel_btn').click()
        self.assertFalse(inputs[0].is_enabled())
