from django.contrib import admin
from .models import UserProfileInfo,Recipe,Comment

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Recipe)
admin.site.register(Comment)
