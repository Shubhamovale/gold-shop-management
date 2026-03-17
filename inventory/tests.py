from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Inventory


class InventoryAPITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='apiuser',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_endpoint_returns_inventory_items(self):
        Inventory.objects.create(
            name='Gold Ring',
            category='gold',
            weight_grams='10.50',
            price='65000.00',
            quantity=2,
            created_by=self.user,
        )

        response = self.client.get(reverse('api_inventory_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Gold Ring')

    def test_create_endpoint_saves_inventory_item(self):
        payload = {
            'name': 'Silver Chain',
            'category': 'silver',
            'weight_grams': '20.00',
            'price': '1500.00',
            'quantity': 4,
            'created_by': self.user.id,
        }

        response = self.client.post(reverse('api_inventory_list'), payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Inventory.objects.count(), 1)

    def test_detail_endpoint_returns_single_item(self):
        item = Inventory.objects.create(
            name='Diamond Pendant',
            category='diamond',
            weight_grams='5.25',
            price='80000.00',
            quantity=1,
            created_by=self.user,
        )

        response = self.client.get(reverse('api_inventory_detail', args=[item.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Diamond Pendant')
