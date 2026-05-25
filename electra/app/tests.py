"""
Unit Test Cases and System Test Cases for Electra E-Commerce Application
IGNOU MCA Project - MCSP-232
Student: Joseph James | Enrolment No: 2452427589
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product, Customer, Cart, Payment, OrderPlaced, ProductReview, ContactUs


# ─────────────────────────────────────────────────────────────────────────────
# UNIT TEST CASES - MODEL TESTS
# ─────────────────────────────────────────────────────────────────────────────
class ProductModelTest(TestCase):
    """Unit tests for the Product model."""
    def setUp(self):
        self.product = Product.objects.create(
            title='Samsung Galaxy S24',
            selling_price=80000.00,
            discounted_price=72000.00,
            description='Latest Samsung flagship smartphone',
            brand='Samsung',
            category='M',
        )

    def test_product_creation(self):
        """TC-UT-01: Test product is created successfully."""
        self.assertEqual(self.product.title, 'Samsung Galaxy S24')
        self.assertEqual(self.product.brand, 'Samsung')

    def test_product_str(self):
        """TC-UT-02: Test product string representation."""
        self.assertEqual(str(self.product), 'Samsung Galaxy S24')

    def test_discount_percentage(self):
        """TC-UT-03: Test discount percentage calculation."""
        expected = round(((80000 - 72000) / 80000) * 100)
        self.assertEqual(self.product.discount_percentage(), expected)

    def test_discount_percentage_zero_price(self):
        """TC-UT-04: Test discount percentage when selling price is zero."""
        self.product.selling_price = 0
        self.assertEqual(self.product.discount_percentage(), 0)


class CustomerModelTest(TestCase):
    """Unit tests for the Customer model."""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='test@test.com'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='Joseph James',
            locality='Pattarkalam House',
            city='Alappuzha',
            mobile=9207380660,
            zipcode=688001,
            state='Kerala',
        )

    def test_customer_creation(self):
        """TC-UT-05: Test customer profile is created successfully."""
        self.assertEqual(self.customer.name, 'Joseph James')
        self.assertEqual(self.customer.state, 'Kerala')

    def test_customer_str(self):
        """TC-UT-06: Test customer string representation."""
        self.assertIn('Joseph James', str(self.customer))


class CartModelTest(TestCase):
    """Unit tests for the Cart model."""
    def setUp(self):
        self.user = User.objects.create_user(username='cartuser', password='pass123')
        self.product = Product.objects.create(
            title='Apple AirPods Pro',
            selling_price=25000.00,
            discounted_price=22000.00,
            description='Wireless earbuds',
            brand='Apple',
            category='H',
        )
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)

    def test_cart_creation(self):
        """TC-UT-07: Test cart item is created successfully."""
        self.assertEqual(self.cart.quantity, 2)
        self.assertEqual(self.cart.product.title, 'Apple AirPods Pro')

    def test_cart_total_cost(self):
        """TC-UT-08: Test cart total cost calculation."""
        expected_total = 2 * 22000.00
        self.assertEqual(self.cart.total_cost, expected_total)

    def test_cart_str(self):
        """TC-UT-09: Test cart string representation."""
        self.assertIn('cartuser', str(self.cart))


class OrderPlacedModelTest(TestCase):
    """Unit tests for the OrderPlaced model."""
    def setUp(self):
        self.user = User.objects.create_user(username='orderuser', password='pass123')
        self.product = Product.objects.create(
            title='Dell Laptop',
            selling_price=65000.00,
            discounted_price=58000.00,
            description='Dell Inspiron 15',
            brand='Dell',
            category='L',
        )
        self.customer = Customer.objects.create(
            user=self.user, name='Test User', locality='Test Locality',
            city='Kochi', mobile=9000000000, zipcode=682001, state='Kerala'
        )
        self.payment = Payment.objects.create(user=self.user, amount=58000.00, paid=True)
        self.order = OrderPlaced.objects.create(
            user=self.user, customer=self.customer,
            product=self.product, quantity=1,
            status='Pending', payment=self.payment
        )

    def test_order_creation(self):
        """TC-UT-10: Test order is created successfully."""
        self.assertEqual(self.order.status, 'Pending')
        self.assertEqual(self.order.quantity, 1)

    def test_order_total_cost(self):
        """TC-UT-11: Test order total cost calculation."""
        self.assertEqual(self.order.total_cost, 58000.00)

    def test_order_str(self):
        """TC-UT-12: Test order string representation."""
        self.assertIn('orderuser', str(self.order))


class ContactUsModelTest(TestCase):
    """Unit tests for the ContactUs model."""
    def test_contact_creation(self):
        """TC-UT-13: Test contact inquiry is saved successfully."""
        contact = ContactUs.objects.create(
            name='John Doe',
            email='john@example.com',
            message='I need help with my order.'
        )
        self.assertEqual(contact.name, 'John Doe')
        self.assertIn('John Doe', str(contact))


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM TEST CASES - VIEW / URL TESTS
# ─────────────────────────────────────────────────────────────────────────────
class HomeViewTest(TestCase):
    """System tests for the home page."""
    def test_home_page_loads(self):
        """TC-ST-01: Test home page returns HTTP 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        """TC-ST-02: Test home page uses correct template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'app/home.html')


class ProductViewTest(TestCase):
    """System tests for product listing and detail views."""
    def setUp(self):
        self.product = Product.objects.create(
            title='Sony Camera',
            selling_price=55000.00,
            discounted_price=49000.00,
            description='Sony Alpha mirrorless camera',
            brand='Sony',
            category='C',
        )

    def test_product_list_loads(self):
        """TC-ST-03: Test product list page returns HTTP 200."""
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_loads(self):
        """TC-ST-04: Test product detail page returns HTTP 200."""
        response = self.client.get(reverse('product-detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_product_search(self):
        """TC-ST-05: Test product search returns correct results."""
        response = self.client.get(reverse('product-list') + '?search=Sony')
        self.assertContains(response, 'Sony Camera')

    def test_product_category_filter(self):
        """TC-ST-06: Test product category filter works correctly."""
        response = self.client.get(reverse('product-list') + '?category=C')
        self.assertContains(response, 'Sony Camera')

    def test_invalid_product_returns_404(self):
        """TC-ST-07: Test accessing non-existent product returns 404."""
        response = self.client.get(reverse('product-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class UserAuthTest(TestCase):
    """System tests for user registration and login."""
    def setUp(self):
        self.user = User.objects.create_user(username='existinguser', password='testpass123')

    def test_register_page_loads(self):
        """TC-ST-08: Test registration page returns HTTP 200."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """TC-ST-09: Test new user can register successfully."""
        self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'StrongPass@123',
            'password2': 'StrongPass@123',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_loads(self):
        """TC-ST-10: Test login page returns HTTP 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        """TC-ST-11: Test user can login with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login(self):
        """TC-ST-12: Test login fails with wrong credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """TC-ST-13: Test user can logout successfully."""
        self.client.login(username='existinguser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


class CartViewTest(TestCase):
    """System tests for cart functionality."""
    def setUp(self):
        self.user = User.objects.create_user(username='carttest', password='pass123')
        self.product = Product.objects.create(
            title='OnePlus Watch',
            selling_price=15000.00,
            discounted_price=12000.00,
            description='Smart watch',
            brand='OnePlus',
            category='S',
        )

    def test_cart_requires_login(self):
        """TC-ST-14: Test cart page redirects unauthenticated users."""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)

    def test_cart_loads_for_logged_in_user(self):
        """TC-ST-15: Test cart page loads for authenticated user."""
        self.client.login(username='carttest', password='pass123')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        """TC-ST-16: Test product can be added to cart."""
        self.client.login(username='carttest', password='pass123')
        self.client.get(reverse('add-to-cart', args=[self.product.pk]))
        self.assertTrue(Cart.objects.filter(user=self.user, product=self.product).exists())

    def test_remove_from_cart(self):
        """TC-ST-17: Test product can be removed from cart."""
        self.client.login(username='carttest', password='pass123')
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        self.client.get(reverse('remove-from-cart', args=[cart_item.pk]))
        self.assertFalse(Cart.objects.filter(pk=cart_item.pk).exists())


class OrderViewTest(TestCase):
    """System tests for order management."""
    def setUp(self):
        self.user = User.objects.create_user(username='ordertest', password='pass123')

    def test_orders_requires_login(self):
        """TC-ST-18: Test orders page redirects unauthenticated users."""
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 302)

    def test_orders_page_loads(self):
        """TC-ST-19: Test orders page loads for authenticated user."""
        self.client.login(username='ordertest', password='pass123')
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)


class ContactViewTest(TestCase):
    """System tests for contact form."""
    def test_contact_page_loads(self):
        """TC-ST-20: Test contact page returns HTTP 200."""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission(self):
        """TC-ST-21: Test contact form saves data correctly."""
        self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@test.com',
            'message': 'This is a test message.',
        })
        self.assertTrue(ContactUs.objects.filter(name='Test User').exists())


class ProfileViewTest(TestCase):
    """System tests for user profile management."""
    def setUp(self):
        self.user = User.objects.create_user(username='profiletest', password='pass123')

    def test_profile_requires_login(self):
        """TC-ST-22: Test profile page redirects unauthenticated users."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_loads(self):
        """TC-ST-23: Test profile page loads for authenticated user."""
        self.client.login(username='profiletest', password='pass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        """TC-ST-24: Test customer profile can be saved."""
        self.client.login(username='profiletest', password='pass123')
        self.client.post(reverse('profile'), {
            'name': 'Profile User',
            'locality': 'Test Locality',
            'city': 'Thrissur',
            'mobile': 9000000001,
            'zipcode': 680001,
            'state': 'Kerala',
        })
        self.assertTrue(Customer.objects.filter(user=self.user).exists())
