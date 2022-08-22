from customers.models import customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=customer
        fields = '__all__'