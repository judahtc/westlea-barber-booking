
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path('login',views.LoginView.as_view(),name="login"),
path('barbers',views.BarberView.as_view(),name="barber"),
path('barber',views.OneBarberView.as_view(),name="updatebarber"),
]