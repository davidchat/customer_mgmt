from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CustomerForm, ProductForm, CreateUserForm
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
	orders = Order.objects.filter(owner=request.user)
	customers = Customer.objects.filter(owner=request.user)
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
	products = Product.objects.filter(owner=request.user)
	context = {'products': products}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def customer(request, pk):
	customer = get_object_or_404(Customer, id=pk)
	# Make sure the customer belongs to the current user.
	if customer.owner != request.user:
		raise Http404
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
	customer = get_object_or_404(Customer, id=pk)
	form = OrderForm(initial={'customer': customer}) 
	form.fields['customer'].queryset = Customer.objects.filter(owner=request.user)
	form.fields['product'].queryset = Product.objects.filter(owner=request.user)
	
	if request.method == 'POST':
		form = OrderForm(data=request.POST)
		form.fields['customer'].queryset = Customer.objects.filter(owner=request.user)
		form.fields['product'].queryset = Product.objects.filter(owner=request.user)
		if form.is_valid():
			new_order = form.save(commit=False)
			new_order.owner = request.user
			new_order.save()
			return redirect('/')

	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def update_order(request, pk):
	order = get_object_or_404(Order, id=pk)
	
	if order.owner != request.user:
		raise Http404
	else:
		if request.method == 'POST':
			form = OrderForm(data=request.POST, instance=order)
			form.fields['customer'].queryset = Customer.objects.filter(owner=request.user)
			form.fields['product'].queryset = Product.objects.filter(owner=request.user)
			if form.is_valid():
				updated_order = form.save(commit=False)
				updated_order.owner = request.user
				updated_order.save()
				return redirect('/')
		else:
			form = OrderForm(instance=order)
			form.fields['customer'].queryset = Customer.objects.filter(owner=request.user)
			form.fields['product'].queryset = Product.objects.filter(owner=request.user)

	context = {'form': form}
	return render(request, 'accounts/update_order.html', context)


@login_required(login_url='login')
def delete_order(request, pk):
	order = get_object_or_404(Order, id=pk)

	if order.owner != request.user:
		raise Http404
	else:
		if request.method == 'POST':
			order.delete()
			return redirect('/')

	context = {'order': order}
	return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login')
def create_customer(request):
	form = CustomerForm

	if request.method == 'POST':
		form = CustomerForm(data=request.POST)
		if form.is_valid():
			new_customer = form.save(commit=False)
			new_customer.owner = request.user
			new_customer.save()
			return redirect('/')

	context = {'form': form}
	return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
def update_customer(request, pk):
	customer = get_object_or_404(Customer, id=pk)
	
	if customer.owner != request.user:
		raise Http404
	else:
		if request.method == 'POST':
			form = CustomerForm(data=request.POST, instance=customer)
			if form.is_valid():
				updated_customer = form.save(commit=False)
				updated_customer.owner = request.user
				updated_customer.save()
				return redirect('/')
		else:
			form = CustomerForm(instance=customer)

	context = {'form': form}
	return render(request, 'accounts/update_customer.html', context)


@login_required(login_url='login')
def delete_customer(request, pk):
	customer = get_object_or_404(Customer, id=pk)

	if customer.owner != request.user:
		raise Http404
	else:
		if request.method == 'POST':
			customer.delete()
			return redirect('/')

	context = {'customer': customer}
	return render(request, 'accounts/delete_customer.html', context)


@login_required(login_url='login')
def create_product(request):
	form = ProductForm

	if request.method == 'POST':
		form = ProductForm(data=request.POST)
		if form.is_valid():
			new_product = form.save(commit=False)
			new_product.owner = request.user
			new_product.save()
			return redirect('products')

	context = {'form': form}
	return render(request, 'accounts/product_form.html', context)


@login_required(login_url='login')
def update_product(request, pk):
	product = get_object_or_404(Product, id=pk)
	
	if product.owner != request.user:
		raise Http404
	else:
		if request.method == 'POST':
			form = ProductForm(data=request.POST, instance=product)
			if form.is_valid():
				updated_product = form.save(commit=False)
				updated_product.owner = request.user
				updated_product.save()
				return redirect('products')
		else:
			form = ProductForm(instance=product)

	context = {'form': form}
	return render(request, 'accounts/update_product.html', context)


@login_required(login_url='login')
def delete_product(request, pk):
	product = get_object_or_404(Product, id=pk)
	if product.owner != request.user:
		raise Http404
	else:
		if request.method == 'POST':
			product.delete()
			return redirect('products')

	context = {'product': product}
	return render(request, 'accounts/delete_product.html', context)


