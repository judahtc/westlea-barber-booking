from rest_framework import serializers
from . import models


class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Barber
        fields = '__all__'