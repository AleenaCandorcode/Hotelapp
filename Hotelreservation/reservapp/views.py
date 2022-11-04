# from requests import request
from django.shortcuts import get_object_or_404
from .serializers import RoomSerializer, UserRegister, HotelSerializer, RoomSerializer
from rest_framework.views import APIView
# from rest_framework.generics import UpdateAPIView
from rest_framework.generics import  CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer

# Create your views here.

class register(APIView):

    def post(self,request,format=None):
        serializer=UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']='registered'
            data['username']=account.username
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
        else:
            data=serializer.errors
        return Response(data)


@api_view(['GET','POST'])
def api_hotel_list_view(request):
    hotel=Hotel.objects.all()
    if request.method =='GET':
        serializer=HotelSerializer(hotel,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        data={}
        serializer=HotelSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            # return 'created Successfully'
            return Response(data,status=status.HTTP_201_CREATED)   
        else:
            # return 'Creation not succesfull'
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

# class RoomDetailView(RetrieveAPIView):
#     serializer_class = RoomSerializer
#     queryset = Room.objects.all()
#     lookup_field = 'room_slug'


@api_view(['GET','POST']) 
def api_room_list_view(request):
    room = Room.objects.all()
    if request.method=='GET':
        data={}
        serializer=RoomSerializer(room,many=True)
        return Response(serializer.data)

    if request.method=='POST':
        data={}
        serializer=RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

