from django.db import models
from django.contrib.auth.models import User
# Create your models here.

MALE = 'Male'
FEMALE = 'Female'
sex_choices = (
    (MALE, MALE),
    (FEMALE, FEMALE)
)

class Sign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    sex = models.CharField(max_length=10, choices=sex_choices)

    def __str__(self):
        return str(self.user)

class RReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.FloatField(null=True,blank=True)
    intensity = models.FloatField(null=True,blank=True)

    def __str__(self):
        return str(self.user)