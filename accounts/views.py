from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm, EditProfileForm, CreateRecipeForm, PasswordChangeCustomForm, \
    UpdateRecipeForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Recipe, UserProfileInfo, Comment, Like
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (ListView, DetailView)
from django.shortcuts import redirect


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
                   'error_Message': errorMessage})


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
                                                   'errorMessage': errorMessage})


def edit_user_profile(request):
    isUpdated = False
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(data=request.POST, instance=request.user)

        if edit_profile_form.is_valid():
            edit_profile_form.save()
            isUpdated = True

        else:
            print(edit_profile_form.errors)

    else:
        edit_profile_form = EditProfileForm(instance=request.user)
        # edit_profile_form.email=request.user

    return render(request, 'accounts/editProfil.html',
                  {'edit_profile_form': edit_profile_form,
                   'isUpdated': isUpdated})


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
                   'isChanged': isChanged})


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
    if request.method == 'POST':
        user_form = CreateRecipeForm(request.POST)
        if user_form.is_valid():
            user = request.user
            userProfile = UserProfileInfo.objects.get(user=user)
            title = user_form.cleaned_data.get('title')
            description = user_form.cleaned_data.get('description')
            instructions = user_form.cleaned_data.get('instructions')
            duration = user_form.cleaned_data.get('duration')
            level = request.POST.get('level')
            ingredients = request.POST.get('hiddenIngList')
            nutrients = request.POST.get('nutrientsTotal')
            # ingredients=""
            # for ing in ingList:
            #    ingredients+="ing"

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
                           'userProfile': userProfile
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
        if request.method == "GET":
            id = self.kwargs.get('user_profile_id')
            userProfile = UserProfileInfo.objects.get(id=id)
            recipes = Recipe.objects.filter(user=userProfile.user)
            if recipes is None:
                errorMessage = "No recipe is created!"
            return render(request, 'accounts/list_recipes.html',
                          {'recipes': recipes,
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
        type = request.GET['type']
        if type == "user":
            users = User.objects.filter(username__icontains=search_term)
            userProfiles = userProfiles.filter(user__in=users)
            displayUser = True
        elif type == "recipe":
            recipes = Recipe.objects.filter(Q(ingredients__icontains=search_term) | Q(title__icontains=search_term))
            displayRecipe = True

    return render(request, 'accounts/search.html',
                  {'userProfiles': userProfiles, 'recipes': recipes, 'displayUser': displayUser,
                   'displayRecipe': displayRecipe})


def user_detail(request, user_profile_id):
    userProfile = UserProfileInfo.objects.get(id=user_profile_id)
    return render(request, 'accounts/user_detail.html', {'userProfile': userProfile})


class RecipeDetailView(DetailView):
    def get(self, request, **kwargs):
        errorMessage = ""
        if request.method == "GET":
            id = self.kwargs.get('pk')
            recipe = Recipe.objects.get(pk=id)
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
            id = self.kwargs.get('pk')
            recipe = Recipe.objects.get(pk=id)
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
                    else:
                        recipe.delete()
                        return redirect(reverse('accounts:list_recipes'))
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


def add_comment(request, user_id, recipe_id):
    errorMessage = ""
    recipe = Recipe.objects.get(pk=recipe_id)
    user = User.objects.get(pk=user_id)
    likes=Like.objects.filter(recipe=recipe)
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
                       'likes':likes
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
    comments=Comment.objects.filter(recipe=recipe)
    likes=Like.objects.filter(recipe=recipe)
    if request.method == "GET":
        alreadyGivenLikes= Like.objects.filter( Q(user=user),Q(recipe=recipe))
        if alreadyGivenLikes.count() == 0:
            Like.objects.create(user=user, recipe=recipe, description="description")
            likes = Like.objects.filter(recipe=recipe)

    return render(request, 'accounts/recipe_just_details.html',
                              {'recipe': recipe,
                               'errorMessage': errorMessage,
                               'comments': comments,
                               'likes': likes
                               })

