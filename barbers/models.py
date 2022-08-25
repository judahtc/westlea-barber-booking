from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

class Barber(models.Model):
    class Meta:
        db_table = 'barber'
        
    national_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=250)
    email_address = models.EmailField(max_length=250)
    
    @property
    def age(self):
        return timesince(self.date_of_birth, timezone.now().today())

    def __str__(self):
        return str(self.national_id)
