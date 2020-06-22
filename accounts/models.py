from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
#from django.contrib.gis.db import models as geoModels
# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type=models.CharField(max_length=50,default="")
    #consumer
    birthday=models.CharField(max_length=50,default="")
    #provider
    provider_name=models.CharField(max_length=50,default="")
    #location = geoModels.PointField()
    address=models.CharField(max_length=50,default="")
    phone_number=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.user.username

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,default="")
    description=models.CharField(max_length=50,default="")
    instructions = models.TextField(max_length=1500,default="")
    duration = models.CharField(max_length=50,default="")
    level=models.CharField(max_length=10,default="")
    ingredients = models.TextField(max_length=50000,default="")
    nutrients = models.TextField(max_length=50000,default="")
    #ingredients = models.OneToOneField('Ingredient', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.CharField(max_length=1000,default="")
    def __str__(self):
        return self.description

class Like(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    description=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.description

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.title


class Meal(models.Model):
    recipe_id = models.IntegerField(default=0)
    title = models.CharField(max_length=50,default="")
    menu_title=models.CharField(max_length=50,default="")
    menu=models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class LikeForMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.description



