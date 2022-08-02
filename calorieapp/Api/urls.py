from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
signup = signUpView.as_view({'post': 'create'}) 
fooditems = foodItemView.as_view({'post': 'create','get':'list'}) 
activities = activityView.as_view({'post': 'create','get':'list'}) 

urlpatterns = [
    path('signup/', signup),
    path('fooditems/', fooditems),
    path('activities/', activities),
    path('login/', loginView.as_view()),
    path('record-food-consumption/', FoodConsumption.as_view()),
    path('record-activity/', ActivityRecord.as_view()),
    path('user-report/', UserReport.as_view()),
]