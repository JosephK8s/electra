from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Product, Customer, Cart, Payment, OrderPlaced, ProductReview, CATEGORY_CHOICES
from .forms import CustomerRegistrationForm, CustomerLoginForm, CustomerProfileForm, ProductReviewForm, ContactUsForm
import razorpay


# ─── Home ─────────────────────────────────────────────────────────────────────
def home(request):
    """Display homepage with all products."""
    products = Product.objects.all()
    return render(request, 'app/home.html', {'products': products})


# ─── Product Views ────────────────────────────────────────────────────────────
def product_detail(request, pk):
    """Display product details and handle review submission."""
    product = get_object_or_404(Product, pk=pk)
    reviews = ProductReview.objects.filter(product=product)
    form = ProductReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Review submitted successfully.')
            return redirect('product-detail', pk=pk)
    return render(request, 'app/productdetail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })


def product_list(request):
    """Display products with optional search and category filter."""
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if search:
        products = products.filter(title__icontains=search)
    return render(request, 'app/productlist.html', {
        'products': products,
        'search': search,
        'category': category,
        'categories': CATEGORY_CHOICES,
    })


# ─── Authentication ───────────────────────────────────────────────────────────
def register(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('home')
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome {user.username}.')
            return redirect('home')
    return render(request, 'app/register.html', {'form': form})


def user_login(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home')
    form = CustomerLoginForm()
    if request.method == 'POST':
        form = CustomerLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    return render(request, 'app/login.html', {'form': form})


def user_logout(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Profile ──────────────────────────────────────────────────────────────────
@login_required
def profile(request):
    """Display and update customer profile."""
    customer = Customer.objects.filter(user=request.user).first()
    form = CustomerProfileForm(instance=customer)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    return render(request, 'app/profile.html', {'form': form, 'customer': customer})


# ─── Cart ─────────────────────────────────────────────────────────────────────
@login_required
def add_to_cart(request, pk):
    """Add a product to the cart."""
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.title} added to cart.')
    return redirect('cart')


@login_required
def cart(request):
    """Display the user's shopping cart."""
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_cost for item in cart_items)
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, pk):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


# ─── Checkout & Payment ───────────────────────────────────────────────────────
@login_required
def checkout(request):
    """Display checkout page with address and order summary."""
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    customer = Customer.objects.filter(user=request.user).first()
    total = sum(item.total_cost for item in cart_items)
    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_data = {'amount': int(total * 100), 'currency': 'INR', 'payment_capture': 1}
    try:
        razorpay_order = client.order.create(data=payment_data)
        razorpay_order_id = razorpay_order['id']
    except Exception:
        razorpay_order_id = 'test_order_id'
    payment = Payment.objects.create(
        user=request.user,
        amount=total,
        razorpay_order_id=razorpay_order_id,
    )
    return render(request, 'app/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'customer': customer,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


@login_required
def payment_done(request):
    """Handle successful payment and place orders."""
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    payment = get_object_or_404(Payment, id=order_id, user=request.user)
    payment.razorpay_payment_id = payment_id
    payment.razorpay_payment_status = 'Paid'
    payment.paid = True
    payment.save()
    customer = Customer.objects.filter(user=request.user).first()
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        OrderPlaced.objects.create(
            user=request.user,
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            payment=payment,
        )
    cart_items.delete()
    messages.success(request, 'Order placed successfully!')
    return redirect('orders')


# ─── Orders ───────────────────────────────────────────────────────────────────
@login_required
def orders(request):
    """Display all orders placed by the user."""
    order_list = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'order_list': order_list})


# ─── Contact ──────────────────────────────────────────────────────────────────
def contact(request):
    """Handle contact form submissions."""
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon.')
            return redirect('contact')
    return render(request, 'app/contact.html', {'form': form})
