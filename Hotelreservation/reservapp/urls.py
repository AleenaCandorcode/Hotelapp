from rest_framework import routers
from reservapp import views
from django.urls import URLPattern, path,include, re_path
from reservapp.views import *


urlpatterns = [
    path('hotel/', api_hotel_list_view,name='hotel-objects'),
    path('room/',api_room_list_view,name='room-objects'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

