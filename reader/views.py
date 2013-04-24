from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.http import HttpResponseRedirect

from reader.forms import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
    else:
        form = RegisterForm()
    return render(request, 'reader/register.html', {'form': form})


def login(request):
    message = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    _login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    message = 'account disabled'
            else:
                message = 'username or login is invalid'
    else:
        form = LoginForm()

    return render(request, 'reader/login.html', {
                  'form': form,
                  'message':  message})


def logout(request):
    _logout(request)
    return HttpResponseRedirect('/')
