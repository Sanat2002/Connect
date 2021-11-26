from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http.response import HttpResponse
from django.shortcuts import render
from .form import LoginForm,RegistrationForm
from django.contrib.auth import get_user_model, login,logout,authenticate

# now create two model classes one that store uuid for verify and other for profile

def login(request):
    iscreatinguser = False

    if request.method == "POST":
        email = request.POST.get("email")
        uname = request.POST.get("username")
        upass = request.POST.get("password")
        if email is not None:
            iscreatinguser = True
            obj1 = RegistrationForm(request.POST)
            if get_user_model().objects.all():
                if get_user_model().objects.get(email=email)==False:
                    if obj1.is_valid():
                        o_obj1 = obj1.save()
                        o_obj1.is_active = False
                        o_obj1.save()
                else:
                    messages.error(request,"Email is already taken...")
            else:
                if obj1.is_valid():
                    o_obj1 = obj1.save()
                    o_obj1.is_active = False
                    o_obj1.save()
        else:
            obj = LoginForm(request=request,data=request.POST)
            print(obj)
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
    if iscreatinguser:
        obj = LoginForm()
        return render(request,"login.html",{"form":obj,"form1":obj1})
    else:
        obj1 = RegistrationForm()
        return render(request,"login.html",{"form":obj,"form1":obj1})