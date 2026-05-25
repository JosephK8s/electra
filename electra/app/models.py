from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('T', 'Tablet'),
    ('C', 'Camera'),
    ('A', 'Accessories'),
    ('S', 'Smart Watch'),
    ('H', 'Headphones'),
    ('G', 'Gaming'),
)

STATE_CHOICES = (
    ('Kerala', 'Kerala'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Karnataka', 'Karnataka'),
    ('Maharashtra', 'Maharashtra'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Rajasthan', 'Rajasthan'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Telangana', 'Telangana'),
)

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)


class Product(models.Model):
    """Represents an electronic product listed in the store."""
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100, default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title

    def discount_percentage(self):
        if self.selling_price > 0:
            return round(((self.selling_price - self.discounted_price) / self.selling_price) * 100)
        return 0


class Customer(models.Model):
    """Stores customer shipping/address details."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Cart(models.Model):
    """Represents items added to a user's shopping cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Payment(models.Model):
    """Records payment transactions via Razorpay."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment by {self.user.username} - Rs.{self.amount}"


class OrderPlaced(models.Model):
    """Represents a confirmed order placed by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS, max_length=50, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class ProductReview(models.Model):
    """Stores customer reviews and ratings for products."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.title}"


class ContactUs(models.Model):
    """Stores customer contact/inquiry form submissions."""
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"
