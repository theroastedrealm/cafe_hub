from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def main_page(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main_page.html', {'posts': posts})


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_page')
    else:
        form = UserProfileForm()
    return render(request, 'create_profile.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('main_page')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def profile_page(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('create_profile')  

    posts = Post.objects.filter(author=request.user)
    return render(request, 'profile_page.html', {'profile': profile, 'posts': posts})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('main_page')
    return render(request, 'delete_post.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('main_page')
    return redirect('main_page')

def user_posts(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    posts = Post.objects.filter(author=user_profile.user).order_by('-created_at')
    return render(request, 'user_posts.html', {'user_profile': user_profile, 'posts': posts})
