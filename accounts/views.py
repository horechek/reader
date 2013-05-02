from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError

from reader.forms import RegisterForm, LoginForm


@login_required
def set_show(request, show_unread):
    profile = request.user.get_profile()
    profile.showUnread = int(show_unread)
    profile.save()
    result = {
        'success': True,
        'showUnread': show_unread
    }
    return HttpResponse(simplejson.dumps(result))


def register(request):
    message = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                HttpResponseRedirect('/')
            except IntegrityError:
                message = 'Error creating user'
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html',
                  {'form': form, 'message': message})


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

    return render(request, 'accounts/login.html', {
                  'form': form,
                  'message':  message})


def logout(request):
    _logout(request)
    return HttpResponseRedirect('/')
