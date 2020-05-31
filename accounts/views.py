from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import(
    User
)
from .serializers import(
    UserSignupSerializer
)
from django.contrib.auth import authenticate,login,logout
from accounts.models import OneSignalNotifications

# Create your views here.
class UserSignupView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]
    def post(self, request):
        if not request.data['player_id']:
            return Response({
                'message':' Player ID missing!'
            },status=403)
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data
            User.objects.create_user(
                password=user_data['password'], 
                username=user_data['username'], 
                full_name=user_data['full_name']
                )
            user = authenticate(username=user_data['username'], password=user_data['password'])
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'user':user,
                'player_id':request.data['player_id'],
            }
            notif = OneSignalNotifications.objects.filter(user=user)
            if notif.exists():
                notif.delete()
                onesig = OneSignalNotifications(**data)
                onesig.save()
            else:
                onesig = OneSignalNotifications(**data)
                onesig.save()
            return Response({
                "message":"User Logged In", 
                "payload":{
                    "id":user.id,
                    "username":user.username,
                    "full_name":user.full_name,
                    "token":token.key,
                    "onesig_id":onesig.player_id
            }},status=201)
        else:
            return Response({"message":serializer.errors}, status=400)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]
    def post(self, request):
        req_data = request.data
        user = authenticate(username=req_data['username'], password=req_data['password'])
        if not user:
            return Response({"message":"Invalid Details"}, status=400)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            if not request.data['player_id']:
                return Response({
                    'message':' Player ID missing!'
                },status=403)
            data = {
                'user':user,
                'player_id':request.data['player_id'],
            }
            notif = OneSignalNotifications.objects.filter(user=user)
            if notif.exists():
                notif.delete()
                onesig = OneSignalNotifications(**data)
                onesig.save()
            else:
                onesig = OneSignalNotifications(**data)
                onesig.save()
            return Response({
                "message":"User Logged In", 
                "payload":{
                    "id":user.id,
                    "username":user.username,
                    "full_name":user.full_name,
                    "token":token.key,
                    "onesig_id":onesig.player_id
            }},status=200)


