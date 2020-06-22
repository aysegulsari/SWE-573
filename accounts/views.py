from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm, EditProfileForm, CreateRecipeForm, PasswordChangeCustomForm, \
    UpdateRecipeForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, UserProfileInfo, Comment, Like, Menu, Meal
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (ListView, DetailView)


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse_lazy("login"))


def register(request):
    registered = False
    errorMessage = ""
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            errorMessage = "Registered"
        else:
            print(user_form.errors, profile_form.errors)
            errorMessage = "Not registered"
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'accounts/signup.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered,
                   'error_Message': errorMessage
                   })


def user_login(request):
    loginFailed = False
    errorMessage = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy("home"))
            else:
                loginFailed = True
                errorMessage = "Your account is not active"
                # return HttpResponse("Your account is not active.")
        else:
            loginFailed = True
            errorMessage = "Invalid login,check your username and password!"
    return render(request, 'accounts/login.html', {'loginFailed': loginFailed,
                                                   'errorMessage': errorMessage
                                                   })


def edit_user_profile(request):
    isUpdated = False
    user = request.user
    userProfile = UserProfileInfo.objects.get(user=user)
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(data=request.POST, instance=request.user)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            isUpdated = True

        else:
            print(edit_profile_form.errors)
        '''
        user.username=request.POST['username']
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']
        user.save()
        '''

    else:
        edit_profile_form = EditProfileForm(instance=request.user)
        # edit_profile_form.email=request.user

    return render(request, 'accounts/editProfile.html',
                  {'edit_profile_form': edit_profile_form,
                   'user': user,
                   'userProfile': userProfile,
                   'isUpdated': isUpdated
                   })


def change_password(request):
    isChanged = False
    if request.method == 'POST':
        change_password_form = PasswordChangeCustomForm(data=request.POST, user=request.user)
        if change_password_form.is_valid():
            change_password_form.save()
            isChanged = True
        else:
            print(change_password_form.errors)
    else:
        change_password_form = PasswordChangeCustomForm(user=request.user)
        # edit_profile_form.email=request.user

    return render(request, 'accounts/changePassword.html',
                  {'change_password_form': change_password_form,
                   'isChanged': isChanged
                   })


def create_recipe(request):
    title = ""
    description = ""
    instructions = ""
    duration = ""
    level = ""
    ingredients = ""
    error_Message = ""
    isOk = ""
    user = request.user
    isConsumer=False
    if request.method == 'POST':
        user_form = CreateRecipeForm(request.POST)
        if user_form.is_valid():
            user = request.user
            userProfile = UserProfileInfo.objects.get(user=user)
            if userProfile.user_type=="consumer":
                isConsumer=True
            title = user_form.cleaned_data.get('title')
            description = user_form.cleaned_data.get('description')
            instructions = user_form.cleaned_data.get('instructions')
            duration = user_form.cleaned_data.get('duration')
            level = request.POST.get('level')
            ingredients = request.POST.get('hiddenIngList')
            nutrients = request.POST.get('nutrientsTotal')

            if ingredients is None:
                error_Message = "First select ingredients!"
                isOk = "First select ingredients!"
            else:
                Recipe.objects.create(user=user, title=title, description=description, instructions=instructions,
                                      duration=duration, level=level, ingredients=ingredients, nutrients=nutrients)
                isOk = "saved with " + ingredients
            recipes = Recipe.objects.filter(user=user)
            return render(request, 'accounts/list_recipes.html',
                          {'recipes': recipes,
                           'errorMessage': error_Message,
                           'userProfile': userProfile,
                           'isConsumer':isConsumer
                           })
            # return HttpResponseRedirect(reverse_lazy("accounts:list_recipes",kwargs={'pk': user.userprofileinfo.id}))
    else:
        user_form = CreateRecipeForm()
        if user_form.is_valid():
            Recipe.objects.create(user=user, title=title, description=description, instructions=instructions,
                                  duration=duration, level=level, ingredients=ingredients)

    return render(request, 'accounts/create_recipe.html',
                  {'user_form': user_form,
                   'title': title,
                   'description': description,
                   'instructions': instructions,
                   'duration': duration,
                   'level': level,
                   'ingredients': ingredients,
                   'error_Message': error_Message,
                   'isOk': isOk,
                   })


class RecipeListView(ListView):
    def get(self, request, **kwargs):
        errorMessage = ""
        isConsumer=False
        if request.method == "GET":
            user_profile_id = self.kwargs.get('user_profile_id')
            userProfile = UserProfileInfo.objects.get(id=user_profile_id)
            if userProfile.user_type=="consumer":
                isConsumer=True
            recipes = Recipe.objects.filter(user=userProfile.user)
            if recipes is None:
                errorMessage = "No recipe is created!"
            return render(request, 'accounts/list_recipes.html',
                          {'recipes': recipes,
                           'errorMessage': errorMessage,
                           'userProfile': userProfile,
                           'isConsumer': isConsumer
                           })


class RecipeDetailView(DetailView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            recipe_id = self.kwargs.get('pk')
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe is None:
                errorMessage = "No recipe is created!"
        return render(request, 'accounts/recipe_details.html',
                      {'recipe': recipe,
                       'errorMessage': errorMessage,
                       })

    def post(self, request, **kwargs):
        errorMessage = ""
        user_form = UpdateRecipeForm(request.POST)
        if request.method == "POST":
            recipe_id = self.kwargs.get('pk')
            recipe = Recipe.objects.get(pk=recipe_id)
            if user_form.is_valid():
                recipe.title = user_form.cleaned_data.get('title')
                recipe.description = user_form.cleaned_data.get('description')
                recipe.instructions = user_form.cleaned_data.get('instructions')
                recipe.duration = user_form.cleaned_data.get('duration')
                recipe.level = request.POST.get('level')
                recipe.ingredients = request.POST.get('hiddenIngList')
                recipe.nutrients = request.POST.get('nutrientsTotal')
                if recipe.ingredients is None:
                    errorMessage = "First select ingredients!"
                else:
                    if request.POST.get("Update"):
                        recipe.save()
                    # else:
                    #    recipe.delete()
                    #    return redirect(reverse('accounts:list_recipes'))
            return render(request, 'accounts/recipe_details.html',
                          {'recipe': recipe,
                           'errorMessage': errorMessage,
                           })


class RecipeJustDetailView(DetailView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            id = self.kwargs.get('pk')
            recipe = Recipe.objects.get(pk=id)
            comments = Comment.objects.filter(recipe=recipe)

            if recipe is None:
                errorMessage = "No recipe is created!"
        return render(request, 'accounts/recipe_just_details.html',
                      {'recipe': recipe,
                       'errorMessage': errorMessage,
                       'comments': comments,
                       })


def add_comment(request, user_id, recipe_id):
    errorMessage = ""
    recipe = Recipe.objects.get(pk=recipe_id)
    user = User.objects.get(pk=user_id)
    likes = Like.objects.filter(recipe=recipe)
    if request.method == "POST":
        comments = Comment.objects.filter(recipe=recipe)
        description = request.POST['comment']
        if description is not None:
            alreadyAddedComments = Comment.objects.filter(Q(description=description), Q(user=user), Q(recipe=recipe))
            if alreadyAddedComments.count() == 0:
                Comment.objects.create(user=user, recipe=recipe, description=description)
                comments = Comment.objects.filter(recipe=recipe)
            return render(request, 'accounts/recipe_just_details.html',
                          {'recipe': recipe,
                           'errorMessage': errorMessage,
                           'comments': comments,
                           'likes': likes
                           })
        return render(request, 'accounts/recipe_just_details.html',
                      {'recipe': recipe,
                       'errorMessage': errorMessage,
                       'comments': comments,
                       'likes': likes
                       })
    return render(request, 'accounts/add_comment.html',
                  {'recipe': recipe,
                   'errorMessage': errorMessage,
                   'user': user,
                   })


def like(request, user_id, recipe_id):
    errorMessage = ""
    recipe = Recipe.objects.get(pk=recipe_id)
    user = User.objects.get(pk=user_id)
    userProfile=UserProfileInfo.objects.get(user=user)
    comments = Comment.objects.filter(recipe=recipe)
    likes = Like.objects.filter(recipe=recipe)
    if request.method == "GET":
        alreadyGivenLikes = Like.objects.filter(Q(user_profile=userProfile), Q(recipe=recipe))
        if alreadyGivenLikes.count() == 0:
            Like.objects.create(user_profile=userProfile, recipe=recipe, description="description")
            likes = Like.objects.filter(recipe=recipe)
    return render(request, 'accounts/recipe_just_details.html',
                  {'recipe': recipe,
                   'errorMessage': errorMessage,
                   'comments': comments,
                   'likes': likes
                   })


def create_menu(request):
    error_Message = ""
    recipes = Recipe.objects.filter(user=request.user)
    menus = Menu.objects.filter(user=request.user)
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfileInfo.objects.get(user=user)
        title = request.POST['title']
        if title is not None:
            menus = Menu.objects.filter(title=title, user=user)
            if not menus:
                Menu.objects.create(title=title, user=user)
                menus = Menu.objects.filter(user=request.user)
        return render(request, 'accounts/list_menus.html',
                      {'menus': menus,
                       'errorMessage': error_Message,
                       'userProfile': userProfile
                       })
    else:
        return render(request, 'accounts/create_menu.html',
                      {'recipes': recipes
                       })


class MenuListView(ListView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            user_profile_id = self.kwargs.get('user_profile_id')
            userProfile = UserProfileInfo.objects.get(id=user_profile_id)
            menus = Menu.objects.filter(user=userProfile.user)
            if menus is None:
                errorMessage = "No menu is created!"
            return render(request, 'accounts/list_menus.html',
                          {'menus': menus,
                           'errorMessage': errorMessage,
                           'userProfile': userProfile,
                           })


def search_list(request):
    userProfiles = UserProfileInfo.objects.all()
    recipes = Recipe.objects.all()
    displayUser = False
    displayRecipe = False
    if 'search' in request.GET:
        search_term = request.GET['search']
        search_type = request.GET['type']
        if search_type == "user":
            users = User.objects.filter(username__icontains=search_term)
            userProfiles = userProfiles.filter(user__in=users)
            displayUser = True
        elif search_type == "recipe":
            recipes = Recipe.objects.filter(Q(ingredients__icontains=search_term) | Q(title__icontains=search_term))
            displayRecipe = True

    return render(request, 'accounts/search.html',
                  {'userProfiles': userProfiles, 'recipes': recipes, 'displayUser': displayUser,
                   'displayRecipe': displayRecipe})


def user_detail(request, user_profile_id):
    isConsumer=False
    userProfile = UserProfileInfo.objects.get(id=user_profile_id)
    if userProfile.user_type == "consumer":
        isConsumer = True
    return render(request, 'accounts/user_detail.html', {'userProfile': userProfile , 'isConsumer': isConsumer})


class MyProfileView(DetailView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            # id = self.kwargs.get('pk')
            user = request.user
            userProfile = UserProfileInfo.objects.get(user=user)
            recipes = Recipe.objects.filter(user=request.user)
            # if recipe is None:
            #    errorMessage="No recipe is created!"
        return render(request, 'accounts/profile.html',
                      {'user': user,
                       'userProfile': userProfile,
                       'recipes': recipes,
                       'errorMessage': errorMessage,
                       })


class MenuDetailView(DetailView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            menu_id = self.kwargs.get('pk')
            menu = Menu.objects.get(pk=menu_id)
            meals = Meal.objects.filter(menu=menu)
            recipes = Recipe.objects.filter(user=request.user)
            if menu is None:
                errorMessage = "No recipe is created!"
        return render(request, 'accounts/menu_details.html',
                      {'menu': menu,
                       'errorMessage': errorMessage,
                       'meals': meals,
                       'recipes': recipes
                       })

    def post(self, request, **kwargs):
        errorMessage = ""
        isUpdated=False
        if request.method == "POST":
            menu_id = self.kwargs.get('pk')
            menu = Menu.objects.get(pk=menu_id)
            meals = Meal.objects.filter(menu=menu)
            recipes = Recipe.objects.filter(user=request.user)

            if request.POST.get("Update"):
                menu.title = request.POST['title']
                menu.save()
                isUpdated=True
            elif request.POST.get("AddRecipe"):
                recipe_id = request.POST['recipe_id']
                if recipes is not None and recipe_id != "0":
                    recipe = Recipe.objects.get(id=recipe_id)
                    meal = Meal.objects.filter(recipe_id=recipe_id, menu__title=menu.title)
                    if not meal:
                        Meal.objects.create(recipe_id=recipe_id, title=recipe.title, menu=menu, menu_title=menu.title)
                meals = Meal.objects.filter(menu=menu)
                recipes = Recipe.objects.filter(user=request.user)
                isUpdated=True
                return render(request, 'accounts/menu_details.html',
                              {'menu': menu,
                               'errorMessage': errorMessage,
                               'meals': meals,
                               'recipes': recipes,
                               'isUpdated':isUpdated
                               })
            else:
                '''
                menu.delete()
                return render(request, 'accounts/profile.html',
                              {'user': request.user,
                               'userProfile': request.user.userProfile,
                               'recipes': recipes,
                               'errorMessage': errorMessage,
                               })'''
            return render(request, 'accounts/menu_details.html',
                          {'menu': menu,
                           'errorMessage': errorMessage,
                           'meals': meals,
                           'recipes': recipes,
                           'isUpdated':isUpdated
                           })


class MenuJustDetailView(DetailView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            id = self.kwargs.get('pk')
            menu = Menu.objects.get(pk=id)
            meals = Meal.objects.filter(menu=menu)
            if menu is None:
                errorMessage = "No recipe is created!"
        return render(request, 'accounts/menu_just_details.html',
                      {'menu': menu,
                       'errorMessage': errorMessage,
                       'meals': meals,
                       })
