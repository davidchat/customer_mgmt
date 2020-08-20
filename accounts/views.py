from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user

@unauthenticated_user
def register_page(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(data=request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account successfully created for ' + username + "!")
			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Incorrect username or password.')

	
	context = {}
	return render(request, 'accounts/login.html', context)


def logout_page(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
		'orders': orders,
		'customers': customers,
		'total_customers': total_customers,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending,
		}
	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	context = {'products': products}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def customer(request, pk):
	customer = get_object_or_404(Customer, id=pk)
	orders = customer.order_set.all()
	order_count = orders.count()

	my_filter = OrderFilter(data=request.GET, queryset=orders)
	orders = my_filter.qs

	context = {
		'customer': customer,
		'orders': orders,
		'order_count':order_count,
		'my_filter': my_filter,
	}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def create_order(request, pk):
	# Set up the inline formset with Parent model, Child model, and fields
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=8)
	customer = get_object_or_404(Customer, id=pk)
	# Queryset argument here takes out previous orders from displayed forms
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer': customer})

	if request.method == 'POST':
		# form = OrderForm(data=request.POST)
		formset = OrderFormSet(data=request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset': formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def update_order(request, pk):
	order = get_object_or_404(Order, id=pk)
	
	if request.method == 'POST':
		form = OrderForm(data=request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = OrderForm(instance=order)

	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def delete_order(request, pk):
	order = get_object_or_404(Order, id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'order': order}
	return render(request, 'accounts/delete_order.html', context)
