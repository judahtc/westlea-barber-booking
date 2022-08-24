from django.db import models

from customers.models import customer
from barbers.models import barber


# Create your models here.
class appointments(models.Model):

    appointmentId=models.AutoField(primary_key=True)
    description=models.CharField(max_length=250)
    serviceType=models.CharField(max_length=250)
    appointDate=models.CharField(max_length=250)
    appointTime=models.CharField(max_length=250)
    amount=models.CharField(max_length=250)
    barberId=models.ForeignKey(barber,on_delete=models.CASCADE)
    custId=models.ForeignKey(customer,on_delete=models.CASCADE)
    class Meta:
        db_table='appointments'
        unique_together = (('appointDate','appointTime','barberId'))


