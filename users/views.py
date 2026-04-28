from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def signup_view(request):
    """
    Handle user registration.

    - Redirects authenticated users to the home page
    - Displays a signup form on GET request
    - Creates a new user and logs them in on successful POST
    """
    # Prevent logged-in users from accessing signup page
    if request.user.is_authenticated:
        return redirect('home')
    
    # Handle form submission
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    """
    Handle user authentication (login).

    - Redirects authenticated users to the home page
    - Displays a login form on GET request
    - Authenticates and logs in the user on successful POST
    """
    # Prevent logged-in users from accessing login page
    if request.user.is_authenticated:
        return redirect('home')

    # Handle login form submission
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})