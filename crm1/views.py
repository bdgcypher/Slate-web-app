from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from django.db.models import Q

# Create your views here.

@unauthenticated_user
def register_page(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user = form.save()

            if user is not None:
                login(request, user)

            messages.success(request, 'Account created for ' + username)
            return redirect('create_customer')

    context = {
        'form': form,

    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def login_page(request):
    form = AuthenticationForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user')

    context = {
        'form': form,

    }
    return render(request, 'accounts/login.html', context)





def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'accounts/home.html', {'products': products})


@login_required(login_url='login')
def customer_home(request):
    products = Product.objects.all()

    context = {
        'products': products,

    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
def profile(request):
    customer = request.user.customer
    orders = request.user.customer.order_set.all()
    order_count = orders.count()

    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'filter': filter,
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='login')
def settings(request):
    customer = request.user.customer
    theme = request.user.customer.theme
    form = ThemeForm(instance=customer)

    if request.method == "POST":
        form = ThemeForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer_home/')

    context = {
        'customer': customer,
        'theme': theme,
        'form': form,
    }

    return render(request, 'accounts/settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    in_production = orders.filter(status='In Production').count()
    shipping = orders.filter(status='Shipping').count()
    delivered = orders.filter(status='Delivered').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'in_production': in_production,
        'shipping': shipping,
        'delivered': delivered,
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def product(request, pk):
    product = Product.objects.get(id=pk)


    return render(request, 'accounts/product.html', {'product': product})


@login_required(login_url='login')
def product2(request, pk):
    product = Product.objects.get(id=pk)


    return render(request, 'accounts/product2.html', {'product': product})


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'filter': filter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def create_order(request, pk):
    order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'size', 'notes', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = order_form_set(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = order_form_set(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/dashboard/')
    context = {
        'formset': formset,
        'customer': customer,
    }
    return render(request, 'accounts/order_form_set.html', context)


@login_required(login_url='login')
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/dashboard/')

    context = {
        'order': order,
    }
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login')
def create_customer(request):
    form = CustomerForm
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
    context = {
        'customer': customer,
        'form': form,
    }
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    user = customer.user
    orders = customer.order_set.all()
    if request.method == "POST":
        orders.delete()
        user.delete()
        customer.delete()
        return redirect('/dashboard/')

    context = {
        'customer': customer,
        'user': user,
        'orders': orders,
    }
    return render(request, 'accounts/delete_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def create_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='login')
def admin_search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        customers = Customer.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q))
        products = Product.objects.filter(Q(name__icontains=q) | Q(category__icontains=q) | Q(price__icontains=q) |
                                          Q(description__icontains=q))
        orders = Order.objects.filter(Q(size__icontains=q) | Q(status__icontains=q) | Q(notes__icontains=q) |
                                      Q(customer__name__icontains=q) | Q(product__name__icontains=q))


        context = {
            'orders': orders,
            'customers': customers,
            'products': products,
            'query': q,
        }
    else:
        context = {}

    return render(request, 'accounts/admin_search.html', context)


def customer_search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(Q(name__icontains=q) | Q(category__icontains=q) | Q(price__icontains=q) |
                                          Q(description__icontains=q))


        context = {
            'products': products,
            'query': q,
        }
    else:
        context = {}

    return render(request, 'accounts/customer_search.html', context)

