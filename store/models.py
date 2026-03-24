from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
import cloudinary.models


# =========================
# Category
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name


# =========================
# Product
# =========================
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    # ⭐ Category
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    # Giá
    price = models.DecimalField(max_digits=10, decimal_places=0)

    # Dùng CloudinaryField thay vì ImageField
    image = cloudinary.models.CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name

    # fallback image
    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        return '/static/store/no-image.png'

    # format giá VN
    @property
    def price_display(self):
        return f"{intcomma(int(self.price)).replace(',', '.')} đ"


# =========================
# Product Image (nhiều ảnh)
# =========================
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = cloudinary.models.CloudinaryField('image')

    def __str__(self):
        return f"Image of {self.product.name}"


# =========================
# Cart
# =========================
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


# =========================
# Cart Item
# =========================
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def total_price_display(self):
        return f"{intcomma(int(self.total_price)).replace('.', ',')} đ"


# =========================
# Order
# =========================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    total = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

    @property
    def total_display(self):
        return f"{intcomma(int(self.total)).replace(',', '.')} đ"


# =========================
# Order Item
# =========================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    @property
    def total_price(self):
        return self.price * self.quantity