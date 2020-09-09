from django.test import TestCase

from accounts.forms import OrderForm, CustomerForm, ProductForm
from accounts.models import Customer, Product, Order


class TestForms(TestCase):

    def setUp(self):
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

    def test_order_form_valid_data(self):
        form = OrderForm(data={
            'customer': self.customer1,
            'product': self.product1,
            'status': 'Pending',
            'note': 'This is a note',
        })

        self.assertTrue(form.is_valid())

    def test_order_form_invalid_status(self):
        form = OrderForm(data={
            'customer': self.customer1,
            'product': self.product1,
            'status': 'Hello',
            'note': 'note',
        })

        self.assertFalse(form.is_valid())

    def test_order_form_no_data(self):
        form = OrderForm(data={})
        
        self.assertFalse(form.is_valid())
        # 3 required fields
        self.assertEqual(len(form.errors), 3)

    def test_customer_form_valid_data(self):
        form = CustomerForm(data={
            'name': 'customer2',
            'phone': '2811234567',
            'email': 'customer2@company.com',
        })

        self.assertTrue(form.is_valid())
    
    def test_customer_form_invalid_phone(self):
        form = CustomerForm(data={
            'name': 'customer2',
            'phone': '2811234567000000000000000',
            'email': 'customer2@company.com',
        })

        self.assertFalse(form.is_valid())

    def test_customer_form_invalid_email(self):
        form = CustomerForm(data={
            'name': 'customer2',
            'phone': '2811234567',
            'email': 'customer2company.com',
        })

        self.assertFalse(form.is_valid())

    def test_customer_form_no_data(self):
        form = CustomerForm(data={})
        
        self.assertFalse(form.is_valid())
        # 3 required fields
        self.assertEqual(len(form.errors), 3)
        
    def test_product_form_valid_data(self):
        form = ProductForm(data={
            'name': 'product2',
            'price': 20.00,
            'category': 'Indoor',
            'description': 'This is Product 2',
        })

        self.assertTrue(form.is_valid())

    def test_product_form_invalid_price(self):
        form = ProductForm(data={
            'name': 'product2',
            'price': 2000000.00,
            'category': 'Indoor',
            'description': 'This is Product 2',
        })

        self.assertFalse(form.is_valid())

    def test_product_form_invalid_category(self):
        form = ProductForm(data={
            'name': 'product2',
            'price': 20.00,
            'category': 'Toys',
            'description': 'This is Product 2',
        })

        self.assertFalse(form.is_valid())
    
    def test_product_form_no_data(self):
        form = ProductForm(data={})
        
        self.assertFalse(form.is_valid())
        # 3 required fields
        self.assertEqual(len(form.errors), 3)


