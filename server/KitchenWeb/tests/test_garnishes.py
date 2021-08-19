import json
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from KitchenWeb.models import Garnish
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, GarnishFactory
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


class GarnishDetailUpdateViewTests(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.garnish = GarnishFactory.create()


    def test_proper_template(self):
        self.assertTemplateUsed("garnishes/detail_update.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:garnish-detail-update", kwargs={'pk': self.garnish.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_garnish(self):
        self.data = {
            "name": "garnish",
            "order": 1,
            "base_price": 100,
        }
        response = self.client.post(reverse('kitchen:garnish-detail-update', kwargs={'pk': self.garnish.pk}),
                                    data=self.data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("kitchen:list_garnish"))
        self.garnish.refresh_from_db()
        self.assertEqual('garnish', self.garnish.name)
        self.assertEqual(1, self.garnish.order)
        self.assertEqual(100, self.garnish.base_price)

