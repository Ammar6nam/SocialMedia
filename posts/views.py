from django.shortcuts import render, redirect
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def post_create (request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST ,files= request.FILES)
        if form.is_valid():
            new_item=form.save(commit=False)
            new_item.user=request.user
            # It sets the user field of the new_item object to the current user who is making the request.
            new_item.save()
            # return redirect('post_list')
    else:
        form=PostCreateForm(data=request.GET) # we must mention GET here to save the photo!
        # form=PostCreateForm()
    return render(request,'posts/create.html',{'form':form})
