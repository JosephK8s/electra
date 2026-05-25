from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, ProductReview, ContactUs


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'category', 'selling_price', 'discounted_price']
    list_filter = ['category', 'brand']
    search_fields = ['title', 'brand']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'city', 'state', 'mobile']
    search_fields = ['name', 'city']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'paid', 'razorpay_order_id']
    list_filter = ['paid']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'status', 'ordered_date']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['user__username', 'product__title']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'submitted_at']
