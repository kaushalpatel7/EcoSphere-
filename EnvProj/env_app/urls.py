from django.urls import path
from . import views
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_view, name='search'),
    path('upload/', views.upload_view, name='upload'),
    path('history/', views.history_view, name='history'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('sustainability-calculator/', views.sustainability_calculator, name='sustainability_calculator'),
    path('order/<int:pk>/', views.order_product, name='order_product'),
    path('orders/', views.orders, name='orders'),
    path('checkout/<str:order_id>/', views.checkout, name='checkout'),

    # Class-based views
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('eco-tips/', views.EcoTipsListView.as_view(), name='eco_tips'),
    path('eco-tips/create/', views.create_eco_tip, name='create_eco_tip'),
    path('eco-tips/<int:pk>/', views.EcoTipDetailView.as_view(), name='eco_tip_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
]