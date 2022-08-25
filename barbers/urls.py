
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('', views.BarbersView.as_view(), name='barbers'),
    path('<str:id>', views.BarberView.as_view(), name='barber'),
    path('barber', views.OneBarberView.as_view(), name='updatebarber'),
]
