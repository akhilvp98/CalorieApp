from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from calorieapp.settings import AUTH_USER_MODEL

userchoices = (
    (1,'ADMIN'),
    (2,'USER')
)

class Labels(models.Model):
    label_name = models.CharField(max_length=255)

class FoodItems(models.Model):
    food_name = models.CharField(max_length=255)
    calories = models.IntegerField()
    label = models.ManyToManyField('Labels')
    approved = models.BooleanField(default=False)

class Activities(models.Model):
    activity_name = models.CharField(max_length=255)
    calorie_burnout = models.IntegerField()
    approved = models.BooleanField(default=False)

class User(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name','username']

    name = models.CharField(max_length=100, null=True, blank=True)
    usertype = models.IntegerField(default=1,choices=userchoices)
    phone_number = models.CharField(unique=True,max_length=15)
    address = models.TextField(max_length=1000,null=True,blank=True)

class UserFoodConsumption(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='food_user')
    food = models.ForeignKey('FoodItems',on_delete=models.CASCADE,related_name='food_food')
    created_at = models.DateTimeField(auto_now_add=True)

class UserActivities(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='activity_user')
    activity = models.ForeignKey('Activities',on_delete=models.CASCADE,related_name='activity_activity')
    created_at = models.DateTimeField(auto_now_add=True)
