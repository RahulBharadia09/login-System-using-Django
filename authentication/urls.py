from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name="signup"),
    path('success/',views.successLogin,name="success"),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    
]
