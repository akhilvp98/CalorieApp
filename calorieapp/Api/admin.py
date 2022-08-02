from django.contrib import admin

from Api.views import FoodConsumption
from .models import *
# Register your models here.
admin.site.register(Labels)
admin.site.register(FoodItems)
admin.site.register(Activities)
admin.site.register(UserFoodConsumption)
admin.site.register(UserActivities)