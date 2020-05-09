from django.db import models
from django.contrib import auth
# Create your models here.
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class User(auth.models.User,auth.models.PermissionsMixin):
    isProvider=models.BooleanField(choices=BOOL_CHOICES,blank=False,default=False)

    def __str__(self):
        return "@{}".format(self.username)
