from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts.views import *


class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register_page)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_page)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_page)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_products_url_resolves(self):
        url = reverse('products')
        self.assertEqual(resolve(url).func, products)

    def test_customer_url_resolves(self):
        url = reverse('customer', args=[1])
        self.assertEqual(resolve(url).func, customer)

    def test_create_order_url_resolves(self):
        url = reverse('create_order', args=['1'])
        self.assertEqual(resolve(url).func, create_order)

    def test_update_order_url_resolves(self):
        url = reverse('update_order', args=['1'])
        self.assertEqual(resolve(url).func, update_order)

    def test_delete_order_url_resolves(self):
        url = reverse('delete_order', args=['1'])
        self.assertEqual(resolve(url).func, delete_order)

    def test_create_customer_url_resolves(self):
        url = reverse('create_customer')
        self.assertEqual(resolve(url).func, create_customer)

    def test_update_customer_url_resolves(self):
        url = reverse('update_customer', args=['1'])
        self.assertEqual(resolve(url).func, update_customer)

    def test_delete_customer_url_resolves(self):
        url = reverse('delete_customer', args=['1'])
        self.assertEqual(resolve(url).func, delete_customer)

    def test_create_product_url_resolves(self):
        url = reverse('create_product')
        self.assertEqual(resolve(url).func, create_product)

    def test_update_product_url_resolves(self):
        url = reverse('update_product', args=['1'])
        self.assertEqual(resolve(url).func, update_product)

    def test_delete_product_url_resolves(self):
        url = reverse('delete_product', args=['1'])
        self.assertEqual(resolve(url).func, delete_product)

   
