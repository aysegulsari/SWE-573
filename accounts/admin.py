from django.contrib import admin
from .models import UserProfileInfo, User,Recipe

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Recipe)
