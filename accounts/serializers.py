from rest_framework import serializers
from .models import User
from rest_framework.fields import CurrentUserDefault

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'full_name', 'password')