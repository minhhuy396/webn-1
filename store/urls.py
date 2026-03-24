from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)