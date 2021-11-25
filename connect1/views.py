import django
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render
from .form import LoginForm
from django.contrib.auth import login,logout,authenticate

# use your own customized form and just take the value from inputs and pass value to the django authentication form to authenticate 

def login(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        upass = request.POST.get("password")
        obj = LoginForm(request=request,data=request.POST)
        if obj.is_valid():
            print(uname,upass)
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,"Successfully Logged In...")
    else:
        obj = LoginForm()
    return render(request,"login.html",{"form":obj})