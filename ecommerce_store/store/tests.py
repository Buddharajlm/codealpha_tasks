from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem


class StoreEcommerceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics', icon='💻')
        self.product = Product.objects.create(
            name='Test Wireless Headphones',
            category=self.category,
            price=Decimal('100.00'),
            stock=10,
            description='Test description'
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')
        self.assertContains(response, '$100.00')

    def test_cart_add_and_detail(self):
        # Add product to cart
        response = self.client.post(reverse('store:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 2})
        self.assertEqual(response.status_code, 302)

        # Check cart detail page
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')
        self.assertContains(response, '$200.00')

    def test_checkout_and_order_processing(self):
        # Add to cart first
        self.client.post(reverse('store:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 2})

        # Submit checkout form
        checkout_data = {
            'full_name': 'Alice Smith',
            'email': 'alice@example.com',
            'phone': '1234567890',
            'address': '456 College Lane',
            'city': 'Boston',
            'state': 'MA',
            'postal_code': '02108',
            'payment_method': 'COD',
            'notes': 'Please call before arrival'
        }
        response = self.client.post(reverse('store:checkout'), data=checkout_data)
        self.assertEqual(response.status_code, 302)

        # Verify Order was created in DB
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.full_name, 'Alice Smith')
        self.assertEqual(order.total_amount, Decimal('200.00')) # Free shipping > $50

        # Verify OrderItem
        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.quantity, 2)

        # Verify stock was decremented from 10 to 8
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

    def test_user_registration(self):
        reg_data = {
            'username': 'bobstudent',
            'email': 'bob@college.edu',
            'password': 'bobpassword123',
            'confirm_password': 'bobpassword123'
        }
        response = self.client.post(reverse('store:register'), data=reg_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='bobstudent').exists())
