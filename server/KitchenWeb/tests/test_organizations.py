from time import sleep
import requests
from accounts.models import Employe, UserToken, Organization
from kitchen5bot.models import TelegramUser

from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome

from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory
from KitchenWeb.views import OrganizationCreateView
from KitchenWeb.views.organizations import OrganizationBalancePageView
from accounts.models import Organization, BalanceChange, Employe, UserToken
from kitchen5bot.models import TelegramUser


class OrganizationsListViewTests(TestCase):
    fixtures = ['organizations_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
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
        self.factory = RequestFactory()
        self.organization = Organization.objects.create(**self.data)
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))

    def test_proper_template(self):
        self.assertTemplateUsed("organizations/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:organization-create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/organizations/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Organization.objects.filter(name='Test Organization').exists())

    def test_post(self):
        self.assertEqual(self.response.status_code, 200)

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
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.driver.get(f'{self.live_server_url}/accounts/{self.token.key}/')

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


    def test_form_disabled_enabled(self):
        self.driver.get(url=f'{self.live_server_url}/organizations/{self.o.pk}')
        inputs = self.driver.find_elements_by_tag_name('input')
        self.assertFalse(inputs[0].is_enabled())
        self.driver.find_element_by_id('edit_btn').click()
        self.assertTrue(inputs[0].is_enabled())
        self.driver.find_element_by_id('cancel_btn').click()
        self.assertFalse(inputs[0].is_enabled())


class OrganizationBalancePageViewTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.path = reverse('kitchen:organization-balance', kwargs={'pk': self.organization.pk})
        self.response = self.client.get(self.path)
        self.client.session['token'] = self.token.key
        self.session = self.client.session
        self.session['token'] = self.token.key

    def test_user_authenticated(self):
        self.assertNotEqual(None, self.session.get('token', None))
        self.assertTrue(UserToken.objects.filter(key=self.session.get('token')).exists())

    def test_proper_template_used(self):
        self.assertTemplateUsed(self.response, 'organizations/balance.html')

    def test_status_200(self):
        self.assertEqual(200, self.response.status_code)

    def test_no_employees(self):
        if self.organization.employe_org.count() < 1:
            self.assertContains(self.response, f'Сотрудники компании "{self.organization.name}" еще не зарегистрированы.')

    def test_form_exists(self):
        if self.organization.employe_org.count() >= 1:
            self.assertContains(self.response, 'обновить баланс')

    def test_accrual(self):
        self.assertEqual(10, self.employee.total_balance)
        data = {"employee": self.employee.id, "type": 'accrual', "comment": 'test comment', "sum_balance": 100}
        response = self.client.post(self.path, data=data)
        self.assertRedirects(response, self.path)
        self.assertEqual(302, response.status_code)
        print(response.status_code)
        self.employee.refresh_from_db()
        self.assertEqual(110, self.employee.total_balance)

    def test_write_off(self):
        self.assertEqual(10, self.employee.total_balance)
        data = {"employee": self.employee.id, "type": 'write-off', "comment": 'test comment', "sum_balance": 5}
        response = self.client.post(self.path, data=data)
        self.assertRedirects(response, self.path)
        self.assertEqual(302, response.status_code)
        self.employee.refresh_from_db()
        self.assertEqual(5, self.employee.total_balance)
