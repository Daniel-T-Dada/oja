from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Avg, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from store.models import Product, Order, Category
from .models import DashboardAnalytics, UserActivity
from django.contrib import messages
from django.http import JsonResponse

def is_admin(user):
    return user.is_superuser

@login_required
def user_dashboard(request):
    # Get user's recent orders
    recent_orders = Order.objects.filter(customer__email=request.user.email).order_by('-date')[:5]
    
    # Get user's activity
    user_activities = UserActivity.objects.filter(user=request.user)[:10]
    
    context = {
        'recent_orders': recent_orders,
        'user_activities': user_activities,
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get date range for analytics
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get analytics for the last 30 days
    analytics = DashboardAnalytics.objects.filter(date__gte=thirty_days_ago).order_by('date')
    
    # Calculate total customers
    total_customers = User.objects.filter(is_superuser=False).count()
    
    # Get recent orders with related data
    recent_orders = Order.objects.select_related('customer', 'product').order_by('-date')[:10]
    
    # Get product statistics
    total_products = Product.objects.count()
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__gt=0, stock__lte=5).count()
    
    # Get top selling products
    top_products = Product.objects.annotate(
        total_orders=Count('order'),
        total_revenue=Sum(F('order__quantity') * F('price'))
    ).order_by('-total_revenue')[:5]
    
    # Get category statistics
    categories = Category.objects.annotate(
        product_count=Count('product'),
        total_sales=Sum('product__order__quantity'),
        total_revenue=Sum(F('product__order__quantity') * F('product__price'))
    )
    
    # Get recent user activities
    recent_activities = UserActivity.objects.select_related('user').all()[:10]
    
    # Calculate revenue trends - Using order_date instead of date for the annotation
    revenue_trend = Order.objects.filter(
        date__date__gte=thirty_days_ago
    ).annotate(
        order_date=TruncDate('date')  # Changed from 'date' to 'order_date'
    ).values('order_date').annotate(  # Changed from 'date' to 'order_date'
        daily_revenue=Sum(F('product__price') * F('quantity')),
        order_count=Count('id')
    ).order_by('order_date')  # Changed from 'date' to 'order_date'
    
    context = {
        'analytics': analytics,
        'recent_orders': recent_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'top_products': top_products,
        'categories': categories,
        'recent_activities': recent_activities,
        'revenue_trend': revenue_trend,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@user_passes_test(is_admin)
def product_management(request):
    products = Product.objects.select_related('category').all().order_by('-id')
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    
    return render(request, 'dashboard/product_management.html', context)

@user_passes_test(is_admin)
def order_management(request):
    orders = Order.objects.select_related('customer', 'product').all().order_by('-date')
    
    # Calculate order statistics
    total_orders = orders.count()
    completed_orders = orders.filter(status=True).count()
    pending_orders = orders.filter(status=False).count()
    total_revenue = orders.aggregate(
        total=Sum(F('product__price') * F('quantity'))
    )['total'] or 0
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'dashboard/order_management.html', context)

@user_passes_test(is_admin)
def customer_management(request):
    customers = User.objects.filter(is_superuser=False).order_by('-date_joined')
    
    # Calculate customer statistics
    total_customers = customers.count()
    active_customers = Order.objects.values('customer').distinct().count()
    new_customers_month = customers.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    context = {
        'customers': customers,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'new_customers_month': new_customers_month,
    }
    
    return render(request, 'dashboard/customer_management.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(customer__email=request.user.email).order_by('-date')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'dashboard/order_history.html', context)

@login_required
def account_settings(request):
    if request.method == 'POST':
        # Handle account settings update
        # Add your account settings update logic here
        messages.success(request, 'Your account settings have been updated successfully.')
        return redirect('account_settings')
    
    return render(request, 'dashboard/account_settings.html')

@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category_id = request.POST.get('category')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            is_sale = request.POST.get('is_sale') == 'on'
            sale_price = request.POST.get('sale_price') if is_sale else 0
            image = request.FILES.get('image')

            if not all([name, category_id, price, stock, description, image]):
                return JsonResponse({
                    'success': False,
                    'error': 'All fields are required'
                })

            category = Category.objects.get(id=category_id)
            
            product = Product.objects.create(
                name=name,
                category=category,
                price=price,
                stock=stock,
                description=description,
                is_sale=is_sale,
                sale_price=sale_price,
                image=image
            )

            # Log the activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='product_added',
                description=f'Added new product: {product.name}'
            )

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Product added successfully!'
                })
            else:
                messages.success(request, 'Product added successfully!')
                return redirect('dashboard:product_management')

        except Category.DoesNotExist:
            error_message = 'Selected category does not exist'
        except Exception as e:
            error_message = str(e)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_message
            })
        else:
            messages.error(request, f'Error adding product: {error_message}')
            return redirect('dashboard:product_management')
    
    return redirect('dashboard:product_management')
