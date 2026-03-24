from django.contrib import admin
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Product, Category, ProductImage, Cart, CartItem, Order, OrderItem


# =========================
# Product Image Inline
# =========================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


# =========================
# Product Admin
# =========================
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_format', 'image_tag')
    inlines = [ProductImageInline]
    fields = ['name','price','category','description','image']

    # ✅ Format giá đẹp
    def price_format(self, obj):
        return f"{intcomma(obj.price).replace(',', '.')} đ"
    price_format.short_description = 'Giá'

    # ✅ Hiển thị ảnh thumbnail
    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" style="border-radius:5px;" />',
                obj.image.url
            )
        return "Không có ảnh"
    image_tag.short_description = 'Ảnh'


# =========================
# Category Admin (có phân cấp)
# =========================
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


# =========================
# Đăng ký admin
# =========================
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)