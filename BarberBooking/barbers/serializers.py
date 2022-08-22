from barbers.models import barber
from rest_framework import serializers

class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model=barber
        fields = '__all__'