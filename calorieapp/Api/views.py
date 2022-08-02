from venv import create
from rest_framework import  viewsets , status
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import date , timedelta
from django.db.models import Sum

class signUpView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = dict()
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            new_data = serializer.data
            new_data.pop('password')
            data['status_code'] = 200
            data['message'] = 'Signup successfull'
            data['data'] = new_data
            return Response({'results':data}, status=status.HTTP_200_OK, headers=headers)
        else:
            data = dict()
            data['status_code'] = 400
            data['message'] = 'Something went wrong!'
            return Response({'results':data}, status=status.HTTP_400_BAD_REQUEST)

class loginView(APIView):
    def post(self,request,*args,**kwargs):
        phone = request.data.get('username')
        password = request.data.get('password')
        data = dict()
        try:
            user = User.objects.get(phone_number=phone,usertype=2)
        except:
            data['status_code'] = 401
            data['message'] = "Login failed"
            return Response({'results':data})
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            new_data = UserSerializer(user,many=False).data
            new_data.pop('password')
            data['status_code'] = 200
            data['message'] = "Succesfully loggedin"
            data['token'] = token.key
            data['data'] = new_data
            return Response({'results':data}, status=status.HTTP_200_OK)
        data['status_code'] = 401
        data['message'] = "Login failed"
        return Response({'results':data})


class foodItemView(viewsets.ModelViewSet):
    queryset = FoodItems.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    serializer_class = FoodItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = dict()
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data['status_code'] = 200
            data['message'] = 'Food Item Created'
            data['data'] = serializer.data
            return Response({'results':data}, status=status.HTTP_200_OK, headers=headers)
        else:
            data = dict()
            data['status_code'] = 400
            data['message'] = 'Something went wrong!'
            return Response({'results':data}, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request,*args,**kwargs):
        data = dict()
        data['status_code'] = 200
        queryset = FoodItems.objects.filter(approved=True).order_by('-id')
        data['data'] = self.serializer_class(queryset,many=True).data
        return Response({'results':data}, status=status.HTTP_200_OK)

class activityView(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    serializer_class = ActivitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = dict()
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data['status_code'] = 200
            data['message'] = 'Activity Created'
            data['data'] = serializer.data
            return Response({'results':data}, status=status.HTTP_200_OK, headers=headers)
        else:
            data = dict()
            data['status_code'] = 400
            data['message'] = 'Something went wrong!'
            return Response({'results':data}, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request,*args,**kwargs):
        data = dict()
        data['status_code'] = 200
        queryset = Activities.objects.filter(approved=True).order_by('-id')
        data['data'] = self.serializer_class(queryset,many=True).data
        return Response({'results':data}, status=status.HTTP_200_OK)

class FoodConsumption(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    def post(self,request,*args,**kwargs):
        food_id = request.data.get('food_id')
        try:
            food = FoodItems.objects.get(id=food_id)
        except:
            return Response({'Error':"Incorrect id"}, status=status.HTTP_400_BAD_REQUEST)
        UserFoodConsumption.objects.create(food=food,user=request.user)
        return Response({'Message':"data added successfully"}, status=status.HTTP_200_OK)       

class ActivityRecord(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    def post(self,request,*args,**kwargs):
        activity_id = request.data.get('activity_id')
        try:
            activity = Activities.objects.get(id=activity_id)
        except:
            return Response({'Error':"Incorrect id"}, status=status.HTTP_400_BAD_REQUEST)
        UserActivities.objects.create(activity=activity,user=request.user)
        return Response({'Message':"data added successfully"}, status=status.HTTP_200_OK)       

class UserReport(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    def get(self,request,*args,**kwargs):
        type = request.query_params.get('type','Today')
        calories_earned = 0
        calories_burned = 0
        if type == "Today":
            today = date.today()
            calories_earned = UserFoodConsumption.objects.filter(user=request.user,created_at__date=today).aggregate(Sum('food__calories'))['food__calories__sum'] 
            calories_burned = UserActivities.objects.filter(user=request.user,created_at__date=today).aggregate(Sum('activity__calorie_burnout'))['activity__calorie_burnout__sum'] 
            data = dict()
        elif type == "LastWeek":
            today = date.today()
            last_week = today - timedelta(days=7)
            calories_earned = UserFoodConsumption.objects.filter(user=request.user,created_at__date__lte=today,created_at__date__gte=last_week).aggregate(Sum('food__calories'))['food__calories__sum'] 
            calories_burned = UserActivities.objects.filter(user=request.user,created_at__date__lte=today,created_at__date__gte=last_week).aggregate(Sum('activity__calorie_burnout'))['activity__calorie_burnout__sum'] 
        elif type == "LastMonth":
            today = date.today()
            last_month = today - timedelta(days=30)
            calories_earned = UserFoodConsumption.objects.filter(user=request.user,created_at__date__lte=today,created_at__date__gte=last_month).aggregate(Sum('food__calories'))['food__calories__sum'] 
            calories_burned = UserActivities.objects.filter(user=request.user,created_at__date__lte=today,created_at__date__gte=last_month).aggregate(Sum('activity__calorie_burnout'))['activity__calorie_burnout__sum'] 
        else:
            return Response({'Error':"Incorrect type"}, status=status.HTTP_400_BAD_REQUEST)
        data = dict()
        data['type'] = type
        data['calories_earned'] = calories_earned
        data['calories_burned'] = calories_burned
        return Response({'results':data}, status=status.HTTP_200_OK)