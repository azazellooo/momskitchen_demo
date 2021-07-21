import json

from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, DishFactory, \
    CategoryFactory
from django.core.files.uploadedfile import SimpleUploadedFile

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
