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

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,default="")
    description=models.CharField(max_length=50,default="")
    instructions = models.TextField(max_length=255,default="")
    duration = models.CharField(max_length=10,default="")
    level=models.CharField(max_length=10,default="")
    ingredients = models.TextField(max_length=100,default="")
    #ingredients = models.OneToOneField('Ingredient', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
