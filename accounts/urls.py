from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('register/', views.register_page, name='register'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<int:pk>/', views.customer, name='customer'),

    path('create-order/<int:pk>/', views.create_order, name='create_order'),
    path('update-order/<int:pk>/', views.update_order, name='update_order'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),

    path('create-customer/', views.create_customer, name='create_customer'),
    path('update-customer/<int:pk>/', views.update_customer, name='update_customer'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete_customer'),

    path('create-product/', views.create_product, name='create_product'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]

