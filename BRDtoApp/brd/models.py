from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    
#One to Many

class BRDReview(models.Model):
    BRD = models.ForeignKey(BRDVarity, on_delete = models.CASCADE, related_name = 'reviews')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.BRD.name}'

#One to One
class brdcertificate(models.Model):
    BRD = models.OneToOneField(BRDVarity, on_delete = models.CASCADE, related_name = 'certificate')
    certificate_number = models.CharField(max_length = 100)
    issued_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f'Certificate for {self.name.BRD}'
        