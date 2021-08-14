from django.test import TestCase
from django.urls import reverse

from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory


class CommandSendTests(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory(id=4)
        self.employee = EmployeeFactory(organization_id=self.organization)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key, 'slug': 's'}))

    def sending_command(self, data):
        response = self.client.post(reverse('kitchen:commands'), **data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('kitchen:commands'))
        response_after_redirect = self.client.get(response.get('Location'))
        self.assertEqual(200, response_after_redirect.status_code)
        self.assertIsNotNone(response_after_redirect.context.get('messages'))

    def test_status_200(self):
        response = self.client.get(reverse('kitchen:commands'))
        self.assertEqual(200, response.status_code)

    def test_create_command(self):
        data = {
            'create_form-organization': [OrganizationFactory(id=i).id for i in range(3)],
            'create-form-text': 'test text'
        }
        self.sending_command(data)

    def test_notification_command(self):
        data = {
            'notification_form-organization':  [OrganizationFactory(id=i).id for i in range(3)],
            'notification_form-text': 'test text'
        }
        self.sending_command(data)

    def test_delivery_arrival_command(self):
        data = {
            'delivery_arrival-organization': [OrganizationFactory(id=i).id for i in range(3)],
            'delivery_arrival-text': 'test text'
        }
        self.sending_command(data)
