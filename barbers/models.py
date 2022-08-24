from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class barber(models.Model):

    barberId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    username=models.CharField(max_length=250)
    password=models.CharField(max_length=250)
    phoneNumber=models.CharField(max_length=250)
    email=models.CharField(max_length=250)
    age=models.CharField(max_length=250)
    
    class Meta:
        db_table='barber'
