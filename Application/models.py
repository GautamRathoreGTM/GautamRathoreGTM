from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.username

class UserDetail(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_of_birth = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)
   
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
