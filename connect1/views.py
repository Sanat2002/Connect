import django
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render
from .form import LoginForm,RegistrationForm
from django.contrib.auth import login,logout,authenticate

def register(request):
    return render(request,"")

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
        obj1 = RegistrationForm()
        obj = LoginForm()
    return render(request,"login.html",{"form":obj,"form1":obj1})

