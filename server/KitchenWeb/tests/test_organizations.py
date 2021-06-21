from django.test import TestCase, RequestFactory
from django.urls import reverse

from KitchenWeb.views import OrganizationCreateView
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
    organization = Organization.objects.create(**data)

    def setUp(self):
        self.factory = RequestFactory()
        Organization.objects.create(**self.data)

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
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Test Organization')

    def test_field_values(self):
        self.assertEqual(self.organization.name, 'Test Organization')
        self.assertEqual(self.organization.address, 'Bishkek')
        self.assertFalse(self.organization.bonus_activation)
        self.assertTrue(self.organization.leave_review)
        self.assertTrue(self.organization.is_active)
        self.assertEqual(self.organization.payment, "('actual', 'фактический расчет')")