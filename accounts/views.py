from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse


@login_required
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})


class LogoutView(View):
    def get(self, request):
        print("LogoutView is being called")
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        #return redirect('login')
        return render(request, 'accounts/logout.html')