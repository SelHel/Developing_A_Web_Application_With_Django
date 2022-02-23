from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate

from .forms import LoginForm, SignupForm


def login_page(request):
    if request.user.is_authenticated:
        messages.success(request, "Vous avez été redirigé.")
        return redirect('flux')
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('flux')
        message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


def signup_page(request):
    if request.user.is_authenticated:
        messages.warning(request, "Vous avez été déconnecté.")
        return redirect('logout')
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie, vous pouvez désormais vous connecter.")
            return redirect('login')

    return render(request, 'authentication/signup.html', context={'form': form})
