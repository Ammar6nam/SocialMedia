from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm, CommentForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from posts import forms as PostEditForm
from .models import Message
from .forms import MessageForm

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            # It sets the user field of the new_item object to the current user who is making the request.
            new_post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('feed')
        else:
            messages.error(request, 'There were errors in the form. Please correct them and try again.')
    else:
        #form = PostCreateForm(data=request.GET)# we must mention GET here to save the photo!
        form = PostCreateForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
def comment_create(request):
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.posted_by = request.user
            try:
                new_comment.save()
            except Exception as e:
                print(f"Error saving comment: {e}")
            return redirect('feed')  # Redirect to the same view
    else:
        comment_form = CommentForm()

    posts = Post.objects.all().order_by('created')
    logged_user = request.user
    context = {
        'posts': posts,
        'logged_user': logged_user,
        'comment_form': comment_form,
    }
    return render(request, 'posts/feed.html', context)


@login_required
def comment_create_userspage(request, username):
    if request.method == "POST":
        comment_form_user = CommentForm(data=request.POST)
        if comment_form_user.is_valid():
            new_comment = comment_form_user.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.posted_by = request.user
            try:
                new_comment.save()
            except Exception as e:
                print(f"Error saving comment: {e}")
            return redirect('userspage', username=username)  # Redirect to the same view
        
    posts = Post.objects.filter(user__username=username).order_by('-created')
    comment_form_user = CommentForm() 
    logged_user = request.user
    context = {
        'posts': posts,
        'logged_user': logged_user,
        'comment_form_user': comment_form_user,
        'username': username,
    }
    return render(request, 'users/userspage.html', context)



@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('userspage')  # Redirect to the 'userspage' after saving the post
    else:
        form = PostEditForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@csrf_protect
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get("post_id")
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                if request.user.is_authenticated:  # Check if user is logged in
                    if post.liked_by.filter(id=request.user.id).exists():
                        post.liked_by.remove(request.user)
                        liked = False
                    else:
                        post.liked_by.add(request.user)
                        liked = True
                    return JsonResponse({'liked': liked})
                else:
                    return JsonResponse({'error': 'You must be logged in to like!'})
            except Post.DoesNotExist:
                return JsonResponse({'error': 'Post not found!'})
        else:
            return JsonResponse({'error': 'Invalid post ID!'})
    return JsonResponse({'error': 'Invalid request!'})


def post_feed(request):
    posts = Post.objects.all()
    for post in posts:
        post.absolute_url = request.build_absolute_uri(post.get_absolute_url())
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            form.save_m2m()  # Save many-to-many relationships (recipients)
            return redirect('inbox')  # Redirect to inbox or another page
    else:
        form = MessageForm()
    return render(request, 'messages/compose.html', {'form': form})