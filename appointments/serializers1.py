from appointments.models import Barber
from rest_framework import serializers

class BarberSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Barber
        fields = ['barberId','username']