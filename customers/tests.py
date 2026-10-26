from django.test import TestCase
from django.urls import reverse
from .models import Customer


class CustomerCRUDTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Alice",
            email="alice@example.com",
            phone="1234567890",
            address="123 Main St",
        )

    def test_customer_list_view(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
        self.assertTemplateUsed(response, 'customers/customer_list.html')

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer-detail', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
        self.assertContains(response, "alice@example.com")
        self.assertTemplateUsed(response, 'customers/customer_detail.html')

    def test_customer_create_view(self):
        response = self.client.post(reverse('customer-create'), {
            'name': 'Bob',
            'email': 'bob@example.com',
            'phone': '9876543210',
            'address': '456 Market St',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(email='bob@example.com').exists())

    def test_customer_update_view(self):
        response = self.client.post(reverse('customer-update', args=[self.customer.pk]), {
            'name': 'Alice Updated',
            'email': 'alice@example.com',
            'phone': '1112223333',
            'address': '789 Oak Ave',
        })
        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Alice Updated')

    def test_customer_delete_view(self):
        response = self.client.post(reverse('customer-delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())
