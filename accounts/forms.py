from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Order, Customer, Product


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['customer', 'product', 'status', 'note']


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'phone', 'email']


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['name', 'price', 'category', 'description']


class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=False)
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


