from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, FriendshipForm, FollowForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Friendship, Follow
from .forms import UserEditForm, ProfileEditForm
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView


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
                return redirect('index')
            else:
                return redirect('login')
    else:
        form= LoginForm()
    return render (request,'users/login.html',{
        'form':form
    })


@login_required
def index (request):
    current_user=request.user
    posts=Post.objects.filter(user=current_user)
    return render (request,'users/index.html',{'posts':posts})


def register(request):
    if request.method == 'POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            # it creates a new user object but doesn't save it to the database yet.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render (request,'users/register_done.html')
    else:
        user_form=UserRegistrationForm()
        return render (request,'users/register.html',{ 'user_form': user_form })    

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
    return render (request,'users/edit.html',{
        'user_form':user_form, 'profile_form':profile_form
    })


class FriendshipListView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = 'friendships/friends_list.html'

    def get_queryset(self):
        return Friendship.objects.filter(from_user=self.request.user)

class CreateFriendshipView(LoginRequiredMixin, CreateView):
    model = Friendship
    form_class = FriendshipForm
    template_name = 'friendships/friends_create.html'

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        return super().form_valid(form)

class FollowListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'follows/follower_list.html'

    def get_queryset(self):
        return Follow.objects.filter(from_user=self.request.user)

class CreateFollowView(LoginRequiredMixin, CreateView):
    model = Follow
    form_class = FollowForm
    template_name = 'follows/follower_create.html'

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        return super().form_valid(form)















# from django.views.generic.edit import CreateView
# from .forms import LoginForm

# class UserLogin(CreateView):
#     form_class=LoginForm
#     template_name='users/login.html'
#     # model=
#     # success_url=