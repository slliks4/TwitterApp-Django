from django.shortcuts import render, get_object_or_404, redirect
from .models import Posts,Comments,Profile
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import Addpost,Edit_model,Edit_profile,Create_profile
from django.contrib import messages
from django.http import HttpResponseRedirect

def home(request):
    posts = Posts.objects.all()
    return render(request, 'index.html', {'posts':posts})

@login_required(login_url='user_login')
def view_post(request,slug):
    user_posts = Posts.objects.get(slug=slug)
    if request.method == 'POST':
        form = Addpost(instance=user_posts, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            raise Http404("invalid")
    else:
        return render(request, 'view_posts.html',{'posts':user_posts})
        
@login_required(login_url='user_login')
def delete_post(request, slug):
    posts = Posts.objects.get(slug=slug)
    if request.method == 'POST':
        user_posts = Posts.objects.get(slug=slug)
        user_posts.delete()
        return redirect('home')
    else:
        return render(request, 'confirm.html',{'posts':posts})

@login_required(login_url='user_login')
def comment(request,slug):
    user_posts = Posts.objects.get(slug = slug)
    comment_posts = get_object_or_404(Posts, slug=slug)
    total_likes = comment_posts.total_likes()
    liked = False
    if comment_posts.likes.filter(id=request.user.id):
        liked = True
    user = request.user
    if not user.is_authenticated:
        raise Http404("The user is not found")
    if request.method == 'POST':
        user_comment = request.POST['user_comments']
        form = Comments(body=user_comment,posts=comment_posts,
                    users=user)
        form.save()
        return redirect('comment', slug=slug)
    else:
        return render(request, 'comment.html',{'post':user_posts,'total_likes':total_likes,'liked':liked})

@login_required(login_url='user_login')
def add_notes(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        status = request.POST['status']
        user = request.user
        if not user.is_authenticated:
            raise Http404("This post has no user")
        form = Posts(title=title,content=content,status=status, users=user)
        form.save()
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        return render(request, 'add_notes.html')
    
@login_required(login_url='user_login')
def like_post(request,slug):
    post = get_object_or_404(Posts, slug=request.POST.get('post_slug'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('comment', args=[str(slug)]))

@login_required(login_url='user_login')
def User_profile(request):
    user = request.user
    if request.method == 'POST':
        form = Edit_model(instance=user,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.info(request, 'invalid')
            return redirect('profile')
    else:
        form = Edit_model(instance=user)
        return render(request, 'profile.html',{'form':form})
    
@login_required(login_url='user_login')
def view_profile(request):
    user = request.user
    profile = get_object_or_404(Profile,users=user)
    return render(request,'view_profile.html',{'profile':profile})

@login_required(login_url='user_login')
def edit_profile(request):
    user = request.user.profile
    if request.method == 'POST':
        form = Edit_profile(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
        else:
            messages.info(request,'invalid')
            return redirect('edit_profile')
    else:
        form = Edit_profile(instance=user)
        return render(request, 'edit_profile.html',{'form':form})
    
@login_required(login_url = 'user_login')
def create_profile(request):
    if request.method == 'POST':
        form = Create_profile(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.users = request.user
            profile.save()
            return redirect('view_profile')
        else:
            raise Http404('invalid')
    else:
        form = Create_profile()
        return render(request, 'create_profile.html',{'form':form})
    
def profile_page(request,id):
    profile = get_object_or_404(Profile, users_id=id)
    return render(request, 'view_profile.html',{'profile':profile})
