
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path('login',views.LoginView.as_view(),name="login"),
path('appointments',views.AppointmentsView.as_view(),name="appointments"),
path('appoint',views.AllAppointsView.as_view(),name="appoint"),
path('appoint/<int:id>',views.OneAppointmentView.as_view(),name="appoint"),
]