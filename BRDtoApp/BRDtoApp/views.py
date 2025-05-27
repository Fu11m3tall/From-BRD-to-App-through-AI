from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    #return HttpResponse("Hello, World. You are all noobs at Home page")
    return render(request, 'website/index.html')

def about(request):
    #return HttpResponse("Hello, World. You are all noobs at About page")
    return render(request, 'website/about.html')

def contact(request):
    #return HttpResponse("Hello, World. You are all noobs at Contact page")
    return render(request, 'website/contact.html')

def services(request):
    #return HttpResponse("Hello, World. You are all noobs at Services page")
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
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'website/signup.html')
            
        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('home')  # Redirect to home page after successful signup
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
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
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')  # Replace 'home' with your actual home route name
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'website/login.html')

    return render(request, 'website/login.html')






