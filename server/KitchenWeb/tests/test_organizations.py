from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory
from KitchenWeb.views import OrganizationCreateView
from accounts.models import Organization, UserToken


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

    def setUp(self):
        self.data = {
            "name": "Test Organization",
            "payment": "actual",
            "address": "Bishkek",
            "bonus_activation": False,
            "leave_review": True,
            "is_active": True
        }
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.request = RequestFactory().post(reverse("kitchen:organization-create"), data=self.data)
        self.middleware = SessionMiddleware()
        self.middleware.process_request(self.request)
        self.request.session.save()
        self.request.session['token'] = self.token.key
        self.response = OrganizationCreateView.as_view()(self.request)
        self.factory = RequestFactory()


    def test_proper_template(self):
        self.assertTemplateUsed("organizations/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:organization-create"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/organizations/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Organization.objects.filter(name=self.organization.name).exists())

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_field_values(self):
        self.assertEqual('Test Organization', self.organization.name)
        self.assertEqual('Bishkek', self.organization.address)
        self.assertFalse(self.organization.bonus_activation)
        self.assertTrue(self.organization.leave_review)
        self.assertTrue(self.organization.is_active)
        self.assertEqual("('actual', 'фактический расчет')", self.organization.payment)


class OrganizationsDetailUpdateViewTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))

    def test_proper_template(self):
        self.assertTemplateUsed("organizations/detail_update.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:organization-detail-update", kwargs={'pk': self.organization.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_organization(self):
        self.data = {
            "name": 'New test Organization',
            "payment": "actual",
            "address": 'Ulan-2',
            "bonus_activation": True,
            "leave_review": True,
            "is_active": True
        }
        response = self.client.post(reverse('kitchen:organization-detail-update', kwargs={'pk': self.organization.pk}),
                                    data=self.data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('kitchen:organization-list'))
        self.organization.refresh_from_db()
        self.assertEqual("New test Organization", self.organization.name)
        self.assertEqual("actual", self.organization.payment)
        self.assertEqual("Ulan-2", self.organization.address)
        self.assertEqual(True, self.organization.bonus_activation)
        self.assertEqual(True, self.organization.leave_review)
        self.assertEqual(True, self.organization.is_active)


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
