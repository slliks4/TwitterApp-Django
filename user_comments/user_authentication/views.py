from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group 
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import Http404


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            def validate_email_address(username):
                try:
                    validate_email(username)
                    return True
                except ValidationError:
                    return False
            if validate_email_address(username):
                raise Http404('invalid')
            else:
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'invalid login details')
                    return redirect('user_login')
        else:
            return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            try:
                group = Group.objects.get(name='users')
            except:
                group = Group.objects.create(name='users')
                group.save()
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'user already exists')
                    return redirect('user_signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email have been registered before')
                    return redirect('user_signup')
                else:
                    new_user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                username=username,email=email,password=password)
                    new_user.groups.add(group)
                    new_user.save()
                    return render(request, 'success.html')
            else:
                messages.info(request, 'password missmatch')
                return redirect('user_signup')
        else:
            return render(request, 'signup.html')
        