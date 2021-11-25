from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http.response import HttpResponse
from django.shortcuts import render
from .form import LoginForm,RegistrationForm
from django.contrib.auth import get_user_model, login,logout,authenticate


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        uname = request.POST.get("username")
        upass = request.POST.get("password")
        obj1 = RegistrationForm(request.POST)
        obj = LoginForm(request=request,data=request.POST)
        if email is not None:
            print(email)
            # if get_user_model().objects.get(email=email)==False:
            print(obj1)
            if obj1.is_valid():
                print("ls")
                obj1.save()
                print("lsss")
            # else:
                # print(email)
            # return HttpResponse("helo")
        else:
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

