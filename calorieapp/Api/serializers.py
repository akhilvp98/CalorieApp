from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name','address', 'phone_number', 'password')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.usertype = 2
        user.username = validated_data.get('phone_number')
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = (
            'id', 'food_name','calories', 'label')

    def create(self, validated_data):
        items = FoodItems.objects.create(food_name= validated_data['food_name'],calories = validated_data['calories'])
        items.label.set(validated_data['label'])
        items.save()
        return items
    
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = (
            'id', 'activity_name','calorie_burnout')

    def create(self, validated_data):
        activity = Activities.objects.create(**validated_data)
        return activity