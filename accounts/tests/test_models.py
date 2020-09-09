from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Customer, Product, Order


class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='1234',
        )
        self.user1.save()

        # Create dummy customer
        self.customer1 = Customer.objects.create(
            name='customer1',
            phone='2811231234',
            email='customer1@company.com',
        )

        # Create dummy product
        self.product1 = Product.objects.create(
            name='product1',
            price=15.00,
            category='Indoor',
            description='This is Product 1',
        )

        self.order1 = Order.objects.create(
            customer=self.customer1,
            product=self.product1,
            status='Pending',
            note='This is Order1'
        )

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer1), 'customer1')

    def test_product_string_representation(self):
        self.assertEqual(str(self.product1), 'product1')

    def test_order_string_representation(self):
        self.assertEqual(str(self.order1), f'{self.customer1.name}: {self.product1.name}')
    


