from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import login,authenticate , logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect,get_object_or_404
from django.core.paginator import Paginator
from App1.models import Log
    




# Create your views here.
def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
 
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')  
    return render(request, "register.html")





def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("blogs")
            
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "login.html")   
    return render(request, "login.html")






def userlogout(request):
    logout(request)
    return redirect('blogs')




def Profile(request):
    return render(request, "profile.html")



def blogs(request):
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(title__icontains=query)
    else:
        posts = BlogPost.objects.all()
   
    
    return render(request, "blog.html", context={'posts':posts, 'query':query})






# def edit_view(request, id):
#     my_object = get_object_or_404(BlogPost, id=id)
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST, instance=my_object)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Blog post updated successfully.')
#             return redirect('blogs')
#     else:
#         form = BlogPostForm(instance=my_object)
#         context = {'form': form}
#         return render(request, 'edit.html', context)

def edit_view(request, id):
    my_object = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=my_object)
        if form.is_valid():
            form.save()
            
            # Log entry after a blog post is updated
            Log.objects.create(action='Updated', user=request.user, post=my_object)
            
            messages.success(request, 'Blog post updated successfully.')
            return redirect('blogs')
    else:
        form = BlogPostForm(instance=my_object)
        context = {'form': form}
        return render(request, 'edit.html', context)


def logs(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'logs.html', {'logs': logs})

# def add_blogs(request):
#     if request.method=="POST":
#         form = BlogPostForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             blogpost = form.save(commit=False)
#             blogpost.author = request.user
#             blogpost.save()
#             obj = form.instance
#             alert = True
#             return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
#     else:
#         form=BlogPostForm()
#     return render(request, "add_blogs.html", {'form':form})
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            
            # Log entry after a blog post is created
            Log.objects.create(action='Created', user=request.user, post=blogpost)
            
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})




from django.contrib import messages

def delete_view(request, id):
    my_object = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        if my_object.author == request.user:
            my_object.delete()
            messages.success(request, 'Blog post deleted successfully.')
            return redirect('blogs')
        else:
            messages.error(request, 'You are not authorized to delete this blog post.')
    else:
        context = {'object': my_object}
        return render(request, 'confirm_delete.html', context)





from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})




from django.contrib.auth.views import PasswordResetView

class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'





from django.views.generic import DetailView
from .models import BlogPost

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog_detail.html"
    context_object_name = "post"


