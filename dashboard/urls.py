from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # User Dashboard URLs
    path('', views.user_dashboard, name='user_dashboard'),
    path('orders/', views.order_history, name='order_history'),
    path('settings/', views.account_settings, name='account_settings'),
    
    # Custom Admin Dashboard URLs (using 'management' instead of 'admin' to avoid conflicts)
    path('management/', views.admin_dashboard, name='admin_dashboard'),
    path('management/products/', views.product_management, name='product_management'),
    path('management/products/add/', views.add_product, name='add_product'),
    path('management/orders/', views.order_management, name='order_management'),
    path('management/customers/', views.customer_management, name='customer_management'),
] 