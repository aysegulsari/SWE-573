from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts.views import RecipeListView,RecipeDetailView,MyProfileView,RecipeJustDetailView

app_name ='accounts'

urlpatterns=[
    path('signup/',views.register,name='signup'),
    path('user_login/',views.user_login,name='user_login'),
    path('edit_user_profile/',views.edit_user_profile,name='edit_user_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('profile_page/',MyProfileView.as_view(),name='profile_page'),
    path('search_page/', views.search_list, name='search_page'),
    path('create_recipe/',views.create_recipe,name='create_recipe'),
    path('list_recipes/<int:user_profile_id>',RecipeListView.as_view(),name='list_recipes'),
    path('myrecipe_details/<int:user_profile_id>/<int:pk>',RecipeDetailView.as_view(),name='my_recipe_details'),
    path('recipe_details/<int:user_profile_id>/<int:pk>', RecipeJustDetailView.as_view(), name='recipe_details'),

    #path('details/<int:poll_id>/', views.poll_detail, name='detail'),
    path('detail/<int:user_profile_id>/', views.user_detail, name='detail'),
]
