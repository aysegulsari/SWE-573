from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserCreationForm(UserCreationForm):

    class Meta:
        fields=('username','first_name','last_name','email','password1','password2','isProvider')
        widgets = {
            'yes_or_no': forms.RadioSelect
        }
        model = User

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='User Name'
        self.fields['email'].label="Email Address"
        self.fields['isProvider'].label="Sign up as a provider"
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
