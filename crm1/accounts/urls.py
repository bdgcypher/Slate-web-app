from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="reset_password"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),

    path('', views.home, name="home"),
    path('customer_home/', views.customer_home, name="user"),
    path('profile/', views.profile, name="profile"),
    path('settings/', views.settings, name="settings"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('products/', views.products, name="products"),
    path('product/<str:pk>/', views.product, name="product"),
    path('user/product/<str:pk>/', views.product2, name="product2"),
    path('customer/<str:pk>/', views.customer, name="customer"),

    path('create_order/<str:pk>/', views.create_order, name="create_order"),
    path('update_order/<str:pk>/', views.update_order, name="update_order"),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),

    path('create_customer/', views.create_customer, name="create_customer"),
    path('update_customer/<str:pk>/', views.update_customer, name="update_customer"),
    path('delete_customer/<str:pk>/', views.delete_customer, name="delete_customer"),

    path('create_product/', views.create_product, name="create_product"),

    path('a_search/', views.admin_search, name="admin_search"),
    path('search/', views.customer_search, name="customer_search"),
]

