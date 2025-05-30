from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def services(request):
    return render(request, 'website/services.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required')
            return render(request, 'website/signup.html')
            
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'website/signup.html')
            
        try:
            # Validate email format
            User.objects.get(email=email)
            messages.error(request, 'Email already exists')
            return render(request, 'website/signup.html')
        except User.DoesNotExist:
            pass
            
        # Validate password strength
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'website/signup.html')
            
        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('login')  # Redirect to login page after successful signup
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'website/signup.html')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
            return render(request, 'website/signup.html')
    
    return render(request, 'website/signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic validation
        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return render(request, 'website/login.html')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  # Use the aliased function
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'website/login.html')

    return render(request, 'website/login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

def brd_upload(request):
    return render(request, 'website/brd-upload.html')





