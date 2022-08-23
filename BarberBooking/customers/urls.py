from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
 path('login',views.LoginView.as_view(),name="login"),
 path('customers',views.CustomerView.as_view(),name="Customer"),
 path('customer',views.OneCustomerView.as_view(),name="updateCustomer"),
 path('appointments',views.AppointmentsView.as_view(),name="CustomerAppointments"),
 path('checkBarbers/<str:date>/<str:time>',views.barberCheckView.as_view(),name="ts"),
  path('barbers',views.BarbersView.as_view(),name="barbs"),  
 
]