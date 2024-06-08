from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

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

def user_logout(request):
    logout(request)
    return render (request,'users/logout.html')

@login_required
def index(request):
    return render (request,'users/index.html')










# from django.views.generic.edit import CreateView
# from .forms import LoginForm

# class UserLogin(CreateView):
#     form_class=LoginForm
#     template_name='users/login.html'
#     # model=
#     # success_url=