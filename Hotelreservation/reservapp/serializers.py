from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.models import User


User=get_user_model()

class UserRegister(serializers.ModelSerializer):

    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=["username","password","email","password2"]

    def save(self):
        reg=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'password does not match'})
        reg.set_password(password)
        reg.save()
        return reg


class HotelSerializer(serializers.ModelSerializer):
    # staff=StaffSerializer()
    class Meta:
        model = Hotel
        fields = '__all__'
        # fields= ('id','hotel_name','address','city','state','pincode','phone')


class RoomSerializer(serializers.ModelSerializer):
    hotel=HotelSerializer
    class Meta:
        model = Room
        # fields = '__all__'
        fields = ('room_no','hotel_name','rate','room_type','is_available')


# from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)