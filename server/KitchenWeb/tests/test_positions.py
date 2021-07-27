import json

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from KitchenWeb.models import Dish, Category
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, DishFactory, \
    CategoryFactory, TelegramUserFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from KitchenWeb.views import PositionCreateView


class PositionListViewTests(TestCase):
    fixtures = ['positions_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:list_position'))


    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_no_positions_response(self):
        if len(self.response.context['dishes']) <= 0:
            self.assertContains(self.response, 'Нет блюд')

    def test_valid_response_for_search_query(self):
        search_field_inner = 'd'
        search_response = self.client.get('/kitchen/position/list/', {'search_value': search_field_inner})
        print(search_response.context)
        [self.assertIn(search_field_inner, dish.name) for dish in search_response.context['dishes']]

    def test_is_paginated_by_5(self):
        self.assertGreaterEqual(5, len(self.response.context['dishes']))


class PositionCreateViewTest(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        x = '{"0.5": {"comment": "Comment", "pricing": "25"}}'
        self.data = {
            "name": "position",
            "description": "position description",
            "category": CategoryFactory(category_name='another category'),
            "base_price": 32323,
            "extra_price": json.loads(x)
        }
        print(type(self.data), self.data)
        print(type(self.data['extra_price']), self.data['extra_price'])
        self.organization = OrganizationFactory()
        self.telegram_user = TelegramUserFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, tg_user=self.telegram_user)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.request = RequestFactory().post(reverse("kitchen:create_position"), data=self.data)
        self.middleware = SessionMiddleware()
        self.middleware.process_request(self.request)
        self.request.session.save()
        self.request.session['token'] = self.token.key
        self.response = PositionCreateView.as_view()(self.request)
        self.factory = RequestFactory()
        self.position = Dish.objects.create(**self.data)

    def test_proper_template(self):
        self.assertTemplateUsed("position/create.html")

    def test_get_request_returns_200(self):
        response = self.client.get(reverse("kitchen:create_position"))
        self.assertEqual(response.status_code, 200)

    def test_proper_path(self):
        self.assertEqual('/kitchen/position/create/', self.request.path)

    def test_create(self):
        self.assertTrue(Dish.objects.filter(name='position').exists())
        self.assertTrue(Dish.objects.filter(description='position description').exists())
        self.assertTrue(Dish.objects.filter(base_price=32323).exists())

    def test_field_values(self):
        self.assertEqual('position', self.position.name)
        self.assertEqual('position description', self.position.description)
        self.assertEqual('another category', self.position.category.category_name)
        self.assertEqual(32323, self.position.base_price)
        self.assertEqual(json.loads('{"0.5": {"comment": "Comment", "pricing": "25"}}'), self.position.extra_price)


class PositionDetailUpdateViewTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.category = CategoryFactory()
        self.position = DishFactory(category=self.category)
        self.response = self.client.get(reverse('kitchen:detail_update_position', kwargs={'pk': self.position.pk}))

    def test_status_200(self):
        self.assertEqual(200, self.response.status_code)
        print(self.response.status_code)

    def test_update_position(self):
        new_jsons = {"0.5": {"comment": "Comment new", "pricing": "30"}}
        new_json = json.dumps(new_jsons)
        data_to_update = {
            'name': DishFactory(name='another test dish name').name,
            'description': 'another test dish description',
            'category': CategoryFactory(category_name='another category').pk,
            'base_price': 214,
            'extra_price': new_json
        }
        print(type(data_to_update), data_to_update)
        response = self.client.post(reverse('kitchen:detail_update_position', kwargs={'pk': self.position.pk}),
                                    data=data_to_update)

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("kitchen:list_position"))
        self.position.refresh_from_db()
        self.assertEqual('another test dish name', self.position.name)
        self.assertEqual('another test dish description', self.position.description)
        self.assertEqual('another category', self.position.category.category_name)
        self.assertEqual(214, self.position.base_price)
        # self.assertEqual(new_json, self.position.extra_price)
