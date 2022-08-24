from . import models
from rest_framework import serializers

class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Barber
        fields = '__all__'