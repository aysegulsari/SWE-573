from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm,EditProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse_lazy("login"))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'accounts/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    loginFailed=False
    errorMessage=""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse_lazy("home"))
            else:
                loginFailed=True
                errorMessage="Your account is not active"
                #return HttpResponse("Your account is not active.")
        else:
            loginFailed=True
            errorMessage="Invalid login,check your username and password!"

    return render(request, 'accounts/login.html', {'loginFailed':loginFailed,
                                                    'errorMessage':errorMessage})

def edit_user_profile(request):
    isUpdated = False
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(data=request.POST,instance=request.user)

        if edit_profile_form.is_valid():
            edit_profile_form.save()
            isUpdated = True

        else:
            print(edit_profile_form.errors)

    else:
        edit_profile_form = EditProfileForm(instance=request.user)
        #edit_profile_form.email=request.user

    return render(request,'accounts/editProfil.html',
                          {'edit_profile_form':edit_profile_form,
                           'isUpdated':isUpdated})


def change_password(request):
    isChanged = False
    if request.method == 'POST':
        change_password_form = PasswordChangeForm(data=request.POST,user=request.user)

        if change_password_form.is_valid():
            change_password_form.save()
            isChanged = True

        else:
            print(change_password_form.errors)

    else:
        change_password_form = PasswordChangeForm(user=request.user)
        #edit_profile_form.email=request.user

    return render(request,'accounts/changePassword.html',
                          {'change_password_form':change_password_form,
                           'isChanged':isChanged})
