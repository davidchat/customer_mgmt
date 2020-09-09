from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.models import Customer, Product, Order


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # Create dummy user
        self.user1 = User.objects.create_user(
            username='user1',
            password='1234',
        )
        self.user1.save()
        
        # Create dummy customer
        self.customer1 = Customer.objects.create(
            name='customer1',
            phone='2811234567',
            email='customer1@company.com',
        )

        # Create dummy product
        self.product1 = Product.objects.create(
            name='product1',
            price=10.00,
            category='Indoor',
            description='The product 1',
        )

        # Create dummy order
        self.order1 = Order.objects.create(
            customer=self.customer1,
            product=self.product1,
            status='Pending',
            note='Order 1 note',
        )

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.products_url = reverse('products')
        self.customer_url = reverse('customer', args=[1])
        self.create_order_url = reverse('create_order', args=['1'])
        self.update_order_url = reverse('update_order', args=['1'])
        self.delete_order_url = reverse('delete_order', args=['1'])
        self.create_customer_url = reverse('create_customer')
        self.update_customer_url = reverse('update_customer', args=['1'])
        self.delete_customer_url = reverse('delete_customer', args=['1'])
        self.create_product_url = reverse('create_product')
        self.update_product_url = reverse('update_product', args=['1'])
        self.delete_product_url = reverse('delete_product', args=['1'])

    def tearDown(self):
        self.client.logout()

    def test_register_get(self):
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    # def test_register_post(self):
    #     response = self.client.post(self.register_url, {
    #         'username': 'user2',
    #         'email': 'user2@company.com',
    #         'password1': '4321',
    #         'password2': '4321',
    #     })
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.last().username, 'user2')

    def test_login_get(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # def test_login_post(self):
    #     response = self.client.post(self.login_url, {
    #         'username': 'user1',
    #         'password': '1234',
    #     })
        
    #     self.assertEqual(str(response.context['user']), 'user1')
    #     self.assertEqual(response.status_code, 302)

    def test_logout_get(self):
        response = self.client.get(self.logout_url)
        
        self.assertEqual(response.status_code, 302)
    
    def test_home_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.home_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_products_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.products_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products.html')

    def test_customer_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.customer_url, args=['1'])

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/customer.html')
        self.assertEqual(Customer.objects.first().name, 'customer1')

    def test_create_order_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.create_order_url, args=['1'])

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/order_form.html')

    # def test_create_order_post(self):
    #     self.client.login(username='user1', password='1234')
    #     response = self.client.post(self.create_order_url,
    #         args=[1],
    #         data={
    #             'product': self.product1,
    #             'status': 'Out for delivery',
    #             'note': 'This is Order 2',
    #         }
    #     )

    #     self.assertEqual(str(response.context['user']), 'user1')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'accounts/order_form.html')
    #     self.assertEqual(self.customer1.order_set.last().note, 'This is Order 2')
        
    def test_create_customer_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.create_customer_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/customer_form.html')

    def test_create_customer_post(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(self.create_customer_url, {
            'name': 'customer2',
            'phone': '2817654321',
            'email': 'customer2@company.com',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.last().name, 'customer2')

    def test_update_customer_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.update_customer_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_customer.html')
        
    def test_update_customer_post(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(self.update_customer_url, {
            'name': 'customerA',
            'phone': '2817654321',
            'email': 'customerA@company.com',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.first().name, 'customerA')
    
    def test_delete_customer_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.delete_customer_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/delete_customer.html')

    def test_delete_customer_post(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(self.delete_customer_url, args=['1'])
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_product_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.create_product_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/product_form.html')

    def test_create_product_post(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(self.create_product_url, {
            'name': 'product2',
            'price': 15.00,
            'category': 'Outdoor',
            'description': 'New Product'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.last().name, 'product2')
        self.assertEqual(Product.objects.last().price, 15.00)
        self.assertEqual(Product.objects.last().category, 'Outdoor')
        self.assertEqual(Product.objects.last().description, 'New Product')

    def test_update_product_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.update_product_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_product.html')
        
    def test_update_product_post(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(self.update_product_url, {
            'name': 'productA',
            'price': 20.00,
            'category': 'Outdoor',
            'description': 'Updated Product',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.first().name, 'productA')
        self.assertEqual(Product.objects.first().price, 20.00)
        self.assertEqual(Product.objects.first().category, 'Outdoor')
        self.assertEqual(Product.objects.first().description, 'Updated Product')
    
    def test_delete_product_get(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(self.delete_product_url)

        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/delete_product.html')

    def test_delete_product_post(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(self.delete_product_url, args=['1'])
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)

