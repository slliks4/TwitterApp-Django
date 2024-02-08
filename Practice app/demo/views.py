from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect
from .models import Profile
from django.contrib import messages
from django.urls import reverse_lazy

def home(request):
    return render(request, 'home.html')

def Profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html',{'profiles':profiles})
    else:
        messages.info(request,'you must be logged in to view this page')
        return redirect('home')

def View_profile(request,id):
    if request.user.is_authenticated:
        profiles = Profile.objects.get(id=id)
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']

            if action == "unfollow":
                current_user_profile.follows.remove(profiles)
            elif action == "follow":
                current_user_profile.follows.add(profiles)
            
            current_user_profile.save()
    else:
        messages.info(request,'you must be logged in to view this page')
        return redirect('home')

    return render(request,'view_profile.html',{'profiles':profiles})

def Search_users(request):
    if request.method == 'POST':
        searched = request.POST['search_users']
        search_users = Profile.objects.filter(bio__contains=searched)
        return render(request, 'search.html',{'search_users':search_users,'searched':searched})
    else:
        return render(request, 'home.html')