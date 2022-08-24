from appointments.models import appointments
from rest_framework import serializers

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=appointments
        fields = '__all__'