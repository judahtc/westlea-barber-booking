from appointments.models import barber
from rest_framework import serializers

class BarberSerializer1(serializers.ModelSerializer):
    class Meta:
        model=barber
        fields = ['barberId','username']