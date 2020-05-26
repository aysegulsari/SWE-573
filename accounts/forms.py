from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo,Recipe

LEVEL_CHOICES= [
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
    ]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('isProvider',)
        widgets = {
            'yes_or_no': forms.RadioSelect
        }

class EditProfileForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email')

class CreateRecipeForm(forms.ModelForm):
    class Meta():
        model = Recipe
        fields = ('title','description','instructions','duration')
