import imp
from multiprocessing import context
from django.shortcuts import redirect, render

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.profile.role=='admin' or request.user.profile.role=='photographer':
            user_obj=request.user.profile
            context={'user_obj':user_obj}
            return render(request,'admin_home.html',context)
    return render(request,'index.html')

def photographer_signup(request):
    pass
    

def user_login(request):
    context={}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        entered_username=request.POST['username']
        entered_password=request.POST['password']
        user=authenticate(request,username=entered_username,password=entered_password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully!")
            return redirect('home')
        else:
            messages.error(request,'Entered username or password is incorrect')
            pass
    return render(request,'users/login.html',context)

@login_required(login_url='user-login')
def user_logour(request):
    logout(request)
    return redirect('user-login')

def user_home(request):
    pass

