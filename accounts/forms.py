from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo,Recipe
from django.contrib.auth.forms import PasswordChangeForm

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
        fields = ('user_type',)


class EditProfileForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email')

class CreateRecipeForm(forms.ModelForm):
    class Meta():
        model = Recipe
        fields = ('title','description','instructions','duration')

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
