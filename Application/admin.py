from django.contrib import admin

from .models import *

# Register your models here.\

class UsersDisplay(admin.ModelAdmin):
    list_display = ["id", "username", "user_email", "password"]

class UsersdetailDisplay(admin.ModelAdmin):
    list_display = ["id", "user_id", "date_of_birth", "mobile", "gender", "address"]

admin.site.register(Users, UsersDisplay)
admin.site.register(UserDetail, UsersdetailDisplay)

