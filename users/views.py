from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import LoginForm
# Create your views here.

class UserLogin(CreateView):
    form_class=LoginForm
    template_name='users/login.html'
    # model=
    # success_url=