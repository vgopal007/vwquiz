# login/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from quizapp.views import user_dashboard
#from quizapp.views import quizapp
from django.contrib.auth.forms import AuthenticationForm # Import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})




def oldlogin_view(request):
    print("In login view of login app")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('user_dashboard') # Redirect to the user_dashboard view
            #return redirect('quizapp')
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    
    print("passing to login.html")
    #return render(request, 'login.html')
    return render(request, 'login/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
    
def oldregister_view(request):
    print("In register_view from login app")
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)  # Automatically log the user in after registration
                return redirect('home')  # Redirect to homepage or dashboard after registration
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'login/register.html')


def register_view(request):
    print("In register_view from login app")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'login/register.html', {'form': form})    