from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import LoginForm, UserRegistrationForm, FriendshipForm, FollowForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .models import Profile, Friendship, Follow, User
from .forms import UserEditForm, ProfileEditForm
from posts.forms import PostCreateForm
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, View
from django.db.models import F


# Create your views here.

#we should here talk about those new packages that we used them : login and authenticate 

def user_login(request):
    # here the type is POST so that means that we need to submit data and our reference here is forms.py

    if request.method =='POST':
        form=LoginForm(request.POST)
            # this one will be checked when we click submit because we configure it in the html file and set the submit method as POST 
        
        if form.is_valid():
            data=form.cleaned_data
            # cleaned_data only contains the data that has been validated by the form. This means that if a field in the form has a validation error, it will not be included in cleaned_data.

            user=authenticate(request,username=data['username'],password=data['password'])
            # The authenticate function checks if the provided username and password match a user in the database. If they do, it returns the user object. If they don't, it returns None.

            if user is not None:
                login(request,user)
                # The login function is a part of the authentication system. It is used to log a user in to create a session for the user.
                # return HttpResponse('user authenticated and logged in')
                return redirect(reverse('userspage', args=[user.username]))
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form= LoginForm()
    return render (request,'users/login.html',{'form':form})



def index(request):
    if request.user.is_authenticated:
        current_user = request.user
        posts = Post.objects.all().order_by('-created')
        profile = Profile.objects.all().first()
        return render(request, 'users/index.html', {'posts': posts, 'profile': profile})
    else:
        public_posts = Post.objects.all().order_by('-created')  # retrieve public posts
        return render(request, 'users/public_index.html', {'posts': public_posts})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


# def register(request):
#     if request.method == 'POST':
#         user_form=UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user=user_form.save(commit=False)
#             # it creates a new user object but doesn't save it to the database yet.
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             return render(request, 'users/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'user_form': user_form})   

@login_required
def edit(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        # instance parameter is used to specify the object that the form should update.
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render (request,'users/edit.html',{'user_form':user_form, 'profile_form':profile_form})


@login_required
def myView(request, username):
    current_user = request.user
    user = User.objects.get(username=username)
    if current_user != user:
        return HttpResponseForbidden()
    posts = Post.objects.filter(user=current_user).order_by('-created')
    profile = Profile.objects.filter(user=current_user).first()

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('userspage',username=current_user.username)  # Redirect to the 'userspage' after saving the post
    else:
        form = PostCreateForm()

    return render(request, 'users/userspage.html', {'posts': posts, 'profile': profile, 'form': form})


class UserListView(ListView):
    model = User
    template_name = 'users/friends_create.html'
    context_object_name = 'users_with_profiles'
    
    def get_queryset(self):
        return User.objects.filter(profile__isnull=False)

class FriendshipListView(ListView):
    model = Friendship
    template_name = 'users/friends_list.html'
    context_object_name = 'friendships'

    def get_queryset(self):
        username = self.kwargs['username']
        self.user = User.objects.get(username=username)
        return Friendship.objects.filter(from_user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class CreateFriendshipView(LoginRequiredMixin, CreateView):
    model = Friendship
    form_class = FriendshipForm
    template_name = 'users/friends_create.html'
    success_url = reverse_lazy('friends_list')  # Redirect URL after successful form submission

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        to_user = User.objects.get(id=self.kwargs['user_id'])
        form.instance.to_user = to_user
        return super().form_valid(form)
    # def form_valid(self, form):
    #     form.instance.from_user = self.request.user
    #     form.instance.to_user_id = self.kwargs['user_id']  # Set the `to_user` based on `user_id` from URL
    #     return super().form_valid(form)
    
class FriendsDeleteView(View):
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            request.user.profile.friends.remove(user)
            return redirect('friends_list')
        except User.DoesNotExist:
            # Handle the case where the user is not found
            return HttpResponseNotFound('User not found')

        

class FollowersListView(ListView):
    model = Friendship
    template_name = 'users/follower_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        username = self.kwargs['username']
        self.user = User.objects.get(username=username)
        return Friendship.objects.filter(to_user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['users_with_profiles'] = User.objects.filter(profile__isnull=False)
        return context
    

class CreateFollowView(LoginRequiredMixin, CreateView):
    model = Follow
    form_class = FollowForm
    template_name = 'users/follower_create.html'

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        return super().form_valid(form)

class FollowDeleteView(View):
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            request.user.profile.follower.remove(user)
            return redirect('follower_list')
        except User.DoesNotExist:
            # Handle the case where the user is not found
            return HttpResponseNotFound('User not found')

def about_view(request):
    return render(request, 'users/about.html')