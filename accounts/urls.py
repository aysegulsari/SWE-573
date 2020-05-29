from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts.views import RecipeListView,RecipeDetailView

app_name ='accounts'

urlpatterns=[
    path('signup/',views.register,name='signup'),
    path('user_login/',views.user_login,name='user_login'),
    path('edit_user_profile/',views.edit_user_profile,name='edit_user_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('create_recipe/',views.create_recipe,name='create_recipe'),
    path('list_recipes/',RecipeListView.as_view(),name='list_recipes'),
    path('list_recipes/<int:pk>',RecipeDetailView.as_view(),name='recipe_details'),
    path('search_ingredient/',views.search_ingredient,name='search_ingredient'),

]
