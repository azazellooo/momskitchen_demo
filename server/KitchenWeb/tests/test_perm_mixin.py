from django.test import TestCase
from django.urls import reverse
from KitchenWeb.tests.factory_boy import OrganizationFactory, EmployeeFactory, UserTokenFactory, SupplementFactory


class AdditionalListViewTests(TestCase):
    fixtures = ['additionals_test_data.json']
    response = None

    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:additional_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:additional_list'))
        self.assertEqual(self.response.status_code, 401)


class AdditionalCreateViewTest(TestCase):
    def setUp(self):

        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:additional_create'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:additional_create'))
        self.assertEqual(self.response.status_code, 401)


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:category_list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:category_list'))
        self.assertEqual(self.response.status_code, 401)


class CategoryCreateViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:category_create'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:category_create'))
        self.assertEqual(self.response.status_code, 401)


class GarnishListViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:list_garnish'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:list_garnish'))
        self.assertEqual(self.response.status_code, 401)


class GarnishCreateViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:create_garnish'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:create_garnish'))
        self.assertEqual(self.response.status_code, 401)

class SupplementListViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:supplement-list'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:supplement-list'))
        self.assertEqual(self.response.status_code, 401)

class SupplementUpdateViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.supplements = SupplementFactory()
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:detail_update_supplement', kwargs={'pk': self.supplements.pk}))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:detail_update_supplement', kwargs={'pk': self.supplements.pk}))
        self.assertEqual(self.response.status_code, 401)

class OfferingCreateViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:offering_create'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:offering_create'))
        self.assertEqual(self.response.status_code, 401)


class OfferingListViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:menu'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:menu'))
        self.assertEqual(self.response.status_code, 200)


class PositionListViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:list_position'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:list_position'))
        self.assertEqual(self.response.status_code, 401)

class OrganizationBalancePageViewTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.employee = EmployeeFactory(organization_id=self.organization, is_admin=True)
        self.token = UserTokenFactory(user=self.employee)
        self.client.get(reverse('profile', kwargs={'token': self.token.key}))
        self.response = self.client.get(reverse('kitchen:organization-balance', kwargs={'pk': self.organization.id}))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_status_code_401(self):
        self.employee.is_admin = False
        self.employee.save()
        self.response = self.client.get(reverse('kitchen:organization-balance', kwargs={'pk': self.organization.id}))
        self.assertEqual(self.response.status_code, 401)
