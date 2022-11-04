from django.db import models
from twilio.rest import Client
from datetime import datetime,date,timedelta
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  



class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    address = models.CharField(max_length=400, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True)
    pincode = models.CharField(max_length=6,null=True)
    # phone=models.CharField(max_length=10)
    description = models.TextField(null=True)

    # staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # city= models.CharField(max_length=200)
    # id=models.IntegerField()

    def __str__(self):
        return self.hotel_name


# def room_images_upload_path(instance, file_name):
#     return f"{instance.room_slug}/room_cover/{file_name}"


# def room_display_images_upload_path(instance, file_name):
#     return f"{instance.room.room_slug}/room_display/{file_name}"

class Room(models.Model):
    ROOM_TYPES = (
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),

    )
    room_no = models.IntegerField(default=101)
    hotel_name = models.ForeignKey(Hotel,null=True,on_delete=models.CASCADE)
    room_type = models.CharField(max_length=200, choices=ROOM_TYPES)
    rate = models.DecimalField(max_digits = 6, decimal_places = 2, null=True)
    # price_per_night = models.DecimalField(max_digits=8, decimal_places=3)
    # cover_image = models.ImageField(upload_to=room_images_upload_path)
    is_available = models.BooleanField(default=3)

    def __str__(self):
        return str(self.room_no)

    def __str__(self):
        return self.hotel_name


class Booking(models.Model):
    # guest_name=models.CharField(max_length=200)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    guest=models.ForeignKey(User,on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    checkin_date=models.DateTimeField(default=datetime.now())
    checkout_date=models.DateTimeField(default=datetime.now() + timedelta(days=1))
    check_out=models.BooleanField(default=False)
    no_of_guests=models.IntegerField(default=1)


    def charge(self):
        if self.check_out:
            if self.checkin_date==self.checkout_date:
                return self.room.rate
            else:
                time_delta = self.checkout_date - self.checkin_date
                total_time = time_delta.days
                total_cost =total_time*self.room.rate
                # return total_cost
                return total_cost
        else:
            return 'calculated when checked out'    


# class RoomDisplayImages(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     display_images = models.ImageField(upload_to=room_display_images_upload_path)

#     def __str__(self):
#         return self.room.room_slug



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
