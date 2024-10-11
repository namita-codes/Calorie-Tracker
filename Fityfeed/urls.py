from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),  # Fix missing comma and remove duplicate
    path('main/', views.main, name='main'),  # Changed path from '' to 'main/'
    path('user/', views.userPage, name='userPage'),
    path('product/', views.fooditem, name='fooditem'),
    path('createfooditem/', views.createfooditem, name='createfooditem'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('addFooditem/', views.addFooditem, name='addFooditem'),
    path('cali/', views.cali, name='cali'),
    path('bmi/', views.bmi, name='bmi'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
