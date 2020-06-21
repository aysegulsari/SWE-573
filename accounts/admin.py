from django.contrib import admin
from .models import UserProfileInfo,Recipe,Comment,Like,Menu,Meal

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Menu)
admin.site.register(Meal)
