from django.test import TestCase, RequestFactory
from django.urls import reverse

from KitchenWeb.tests.factory_boy import EmployeeFactory, UserTokenFactory
from accounts.models import UserToken


class UserProfileViewTest(TestCase):

    def setUp(self):
        self.employee = EmployeeFactory()
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('profile_distoken'))
        self.session = self.client.session
        self.session['token'] = self.token.key

    def test_user_authenticated(self):
        self.assertNotEqual(None, self.session.get('token', None))
        self.assertTrue(UserToken.objects.filter(key=self.session.get('token')).exists())

    def test_proper_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/profile.html')


    def test_status_200(self):
        self.assertEqual(200, self.response.status_code)






