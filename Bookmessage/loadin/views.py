from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from django.conf import settings
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create_user(username=username, password=password, email=email,)
            user_profile = UserProfile(user=user)
            user_profile.save()
        return HttpResponseRedirect("/accounts/login/")
    else:
        form = RegistrationForm()
    return render(request, 'loadin/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('loadin:profile', args=[user.id]))

            else:
                return render(request, 'loadin/login.html', {'form': form, 'message': 'Wrong password. Please try again.'})

    else:
        form = LoginForm()

    return render(request, 'loadin/login.html', {'form': form})


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'loadin/profile.html', {'user': user})


def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.address = form.cleaned_data['address']
            user_profile.save()

        return HttpResponseRedirect(reverse('loadin:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, 'address': user_profile.address}
        form = ProfileForm(default_data)

    return render(request, 'loadin/profile_update.html', {'form': form, 'user': user})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/accounts/login/")

            else:
                return render(request, 'loadin/pwd_change.html', {'form': form, 'user': user, 'message': 'Old password is wrong.Try again'})
    else:
        form = PwdChangeForm()

    return render(request, 'loadin/pwd_change.html', {'form': form, 'user': user})
