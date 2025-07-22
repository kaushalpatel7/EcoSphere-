from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .forms import OrderForm
import uuid
from django.urls import reverse
from django.views.decorators.http import require_POST
# import requests

from .models import EcoProduct, EcoTip, UserUpload, UserHistory, SustainabilityCalculator, Order
from .forms import UserRegistrationForm, UserUploadForm, SustainabilityCalculatorForm
from .forms import EcoTipForm, ProfileForm
from django.contrib import messages
from .forms import ContactForm


# Class-based views
class ProductListView(LoginRequiredMixin, ListView):
    model = EcoProduct
    template_name = 'env_app_dir/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    login_url = 'login'
    redirect_field_name = 'next'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = EcoProduct
    template_name = 'env_app_dir/product_detail.html'
    context_object_name = 'product'
    login_url = 'login'
    redirect_field_name = 'next'


class EcoTipsListView(ListView):
    model = EcoTip
    template_name = 'env_app_dir/eco_tips.html'
    context_object_name = 'tips'
    paginate_by = 10


class EcoTipDetailView(DetailView):
    model = EcoTip
    template_name = 'env_app_dir/eco_tip_detail.html'
    context_object_name = 'tip'


# Class-based views
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = EcoProduct.objects.all()[:6]
        context['tips'] = EcoTip.objects.all()[:3]
        request = self.request
        if request.user.is_authenticated:
            UserHistory.objects.create(
                user=request.user,
                page_visited='Home',
                session_id=request.session.session_key
            )
        return context


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next', request.POST.get('next', ''))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')


# View for creating eco tips
from django.contrib.auth.decorators import login_required

@login_required
def create_eco_tip(request):
    if request.method == 'POST':
        form = EcoTipForm(request.POST, request.FILES)
        if form.is_valid():
            eco_tip = form.save(commit=False)
            eco_tip.author = request.user
            eco_tip.save()
            messages.success(request, 'Eco tip added successfully!')
            return redirect('eco_tips')
    else:
        form = EcoTipForm()
    return render(request, 'env_app_dir/create_eco_tip.html', {'form': form})


@login_required
def dashboard(request):
    user_uploads = UserUpload.objects.filter(user=request.user)[:5]
    recent_history = UserHistory.objects.filter(user=request.user).order_by('-visit_date')[:10]

    # Track dashboard visit
    UserHistory.objects.create(
        user=request.user,
        page_visited='Dashboard',
        session_id=request.session.session_key
    )

    context = {
        'user_uploads': user_uploads,
        'recent_history': recent_history,
    }
    return render(request, 'dashboard.html', context)


def search_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    products = EcoProduct.objects.all()
    tips = EcoTip.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
        tips = tips.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        products = products.filter(category=category)
        tips = tips.filter(category=category)

    # Track search
    if request.user.is_authenticated:
        UserHistory.objects.create(
            user=request.user,
            page_visited=f'Search: {query}',
            session_id=request.session.session_key
        )

    context = {
        'products': products,
        'tips': tips,
        'query': query,
        'category': category,
    }
    return render(request, 'search.html', context)


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('dashboard')
    else:
        form = UserUploadForm()

    return render(request, 'upload.html', {'form': form})


@login_required
def history_view(request):
    user_history = UserHistory.objects.filter(user=request.user).order_by('-visit_date')

    # Group by date
    visits_by_date = {}
    for visit in user_history:
        date = visit.visit_date.date()
        if date not in visits_by_date:
            visits_by_date[date] = []
        visits_by_date[date].append(visit)

    context = {
        'visits_by_date': visits_by_date,
        'total_visits': user_history.count(),
    }
    return render(request, 'history.html', context)


@login_required
def sustainability_calculator(request):
    if request.method == 'POST':
        form = SustainabilityCalculatorForm(request.POST)
        if form.is_valid():
            calculator = form.save(commit=False)
            calculator.user = request.user

            # Calculate carbon footprint (simplified calculation)
            electricity_factor = 0.92  # kg CO2 per kWh
            water_factor = 0.298  # kg CO2 per gallon
            waste_factor = 2.53  # kg CO2 per pound
            transport_factor = 0.404  # kg CO2 per mile

            carbon_footprint = (
                    calculator.electricity_usage * electricity_factor +
                    calculator.water_usage * water_factor +
                    calculator.waste_production * waste_factor +
                    calculator.transportation_miles * transport_factor
            )

            calculator.carbon_footprint = carbon_footprint
            calculator.save()

            messages.success(request, f'Your carbon footprint: {carbon_footprint:.2f} kg CO2/year')
            return redirect('sustainability_calculator')
    else:
        form = SustainabilityCalculatorForm()

    # Get user's previous calculations
    previous_calculations = SustainabilityCalculator.objects.filter(user=request.user).order_by('-calculated_at')[:5]

    context = {
        'form': form,
        'previous_calculations': previous_calculations,
    }
    return render(request, 'env_app_dir/ustainability_calculator.html', context)

def eco_tips(request):
    blogs = [
        {
            "title": "Use LED lighting throughout your home",
            "content": "Switching to LED lighting can reduce your energy consumption and carbon emissions. LED bulbs are up to 90% more efficient than traditional bulbs and last much longer. [Read more](https://www.greenmatch.co.uk/blog/how-to-be-more-eco-friendly)"
        },
        {
            "title": "Eat Less Meat",
            "content": "Reducing your meat consumption can significantly lower your carbon footprint. Try incorporating more plant-based meals into your diet. [Read more](https://www.greenmatch.co.uk/blog/how-to-be-more-eco-friendly)"
        },
        {
            "title": "Use Public Transport",
            "content": "Using public transport instead of a car helps reduce air pollution and greenhouse gas emissions. Consider walking or cycling for short trips. [Read more](https://www.greenmatch.co.uk/blog/how-to-be-more-eco-friendly)"
        },
        {
            "title": "Upgrade to Energy Efficient Appliances",
            "content": "When it's time to replace appliances, choose energy-efficient models. Look for the energy label to ensure you are making a greener choice. [Read more](https://www.greenmatch.co.uk/blog/how-to-be-more-eco-friendly)"
        },
        {
            "title": "Use Eco-Cleaning Products",
            "content": "Switch to cleaning products made from natural ingredients to reduce water pollution and protect biodiversity. You can also make your own cleaners using vinegar, lemon juice, and baking soda. [Read more](https://www.greenmatch.co.uk/blog/how-to-be-more-eco-friendly)"
        },
    ]
    return render(request, 'env_app_dir/eco_tips.html', {'blogs': blogs})


@login_required
def order_product(request, pk):
    product = get_object_or_404(EcoProduct, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.order_id = str(uuid.uuid4())[:8].upper()
            order.save()
            total_amount = product.price * order.quantity
            return redirect('checkout', order_id=order.order_id)
    else:
        form = OrderForm()
    return render(request, 'order_product.html', {'form': form, 'product': product})

@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    total_amount = order.product.price * order.quantity
    return render(request, 'checkout.html', {'order': order, 'total_amount': total_amount})

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders.html', {'orders': user_orders})

def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent! We'll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(EcoProduct, pk=pk)
    cart = request.session.get('cart', {})
    product_id = str(product.pk)
    quantity = int(request.POST.get('quantity', 1))
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else '',
            'quantity': quantity,
        }
    request.session['cart'] = cart
    return JsonResponse({'success': True, 'cart': cart})

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'image': item['image'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def update_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(pk)
        quantity = int(request.POST.get('quantity', 1))
        if product_id in cart:
            if quantity > 0:
                cart[product_id]['quantity'] = quantity
            else:
                del cart[product_id]
            request.session['cart'] = cart
        return JsonResponse({'success': True, 'cart': cart})
    return JsonResponse({'success': False})

@login_required
def remove_from_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(pk)
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
        return JsonResponse({'success': True, 'cart': cart})
    return JsonResponse({'success': False})

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart_items = []
        order_ids = []
        for product_id, item in cart.items():
            product = EcoProduct.objects.get(pk=product_id)
            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=item['quantity'],
                order_id=str(uuid.uuid4())[:8].upper()
            )
            order_ids.append(order.order_id)
            cart_items.append({
                'name': item['name'],
                'image': item['image'],
                'price': item['price'],
                'quantity': item['quantity'],
                'subtotal': item['price'] * item['quantity'],
            })
        request.session['cart'] = {}
        request.session['last_order'] = {'orders': order_ids, 'items': cart_items, 'total': sum(i['subtotal'] for i in cart_items)}
        return redirect('order_confirmation')
    return redirect('cart_view')

@login_required
def order_confirmation(request):
    last_order = request.session.get('last_order')
    if not last_order:
        return redirect('cart_view')
    return render(request, 'order_confirmation.html', last_order)