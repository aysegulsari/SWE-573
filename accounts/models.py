from django.db import models
from django.contrib.auth.models import User
# Create your models here.
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isProvider=models.BooleanField(choices=BOOL_CHOICES,blank=False,default=False)

    def __str__(self):
        return self.user.username
