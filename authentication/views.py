from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate

from . import forms


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        form.save()
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(request, new_user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    form = forms.SignupForm()

    return render(request, 'authentication/signup.html', context={'form': form})
