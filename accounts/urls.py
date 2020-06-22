from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts.views import RecipeListView, RecipeDetailView, MyProfileView, RecipeJustDetailView, MenuListView, MenuDetailView, MenuJustDetailView

app_name ='accounts'

urlpatterns=[
    path('signup/', views.register, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile_page/', MyProfileView.as_view(), name='profile_page'),
    path('search_page/', views.search_list, name='search_page'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('create_menu/', views.create_menu, name='create_menu'),
    path('list_recipes/<int:user_profile_id>', RecipeListView.as_view(), name='list_recipes'),
    path('list_menus/<int:user_profile_id>', MenuListView.as_view(), name='list_menus'),
    path('myrecipe_details/<int:user_profile_id>/<int:pk>', RecipeDetailView.as_view(), name='my_recipe_details'),
    path('recipe_details/<int:user_profile_id>/<int:pk>', RecipeJustDetailView.as_view(), name='recipe_details'),
    path('mymenu_details/<int:user_profile_id>/<int:pk>', MenuDetailView.as_view(), name='my_menu_details'),
    path('menu_details/<int:user_profile_id>/<int:pk>', MenuJustDetailView.as_view(), name='menu_details'),
    path('add_comment/<int:user_id>/<int:recipe_id>', views.add_comment, name='add_comment'),
    path('like/<int:user_id>/<int:recipe_id>', views.like, name='like'),
    path('detail/<int:user_profile_id>/', views.user_detail, name='detail'),
]
