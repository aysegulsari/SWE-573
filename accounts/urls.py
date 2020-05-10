from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name ='accounts'

urlpatterns=[
    path('signup/',views.register,name='signup'),
    path('user_login/',views.user_login,name='user_login'),
    path('edit_user_profile/',views.edit_user_profile,name='edit_user_profile'),
]
