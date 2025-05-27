from django.db import models
from django.utils import timezone

# Create your models here.
class BRDVarity(models.Model):
    BRD_TYPE_CHOICE = [
        ('BRD', 'BRD'),
        ('KM', 'KAAM'),
        ('HW', 'HELLOWORLD'),
        ('SG', 'SWIGGY'),
        ('OLA', 'OLA'),
        ('UB', 'UBER'),
        ('ZM', 'ZOMATO'),
    ]

    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'BRDs/')
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length = 10, choices = BRD_TYPE_CHOICE)

    description = models.TextField(default='')
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'BRD Variety'
        verbose_name_plural = 'BRD Varieties'
