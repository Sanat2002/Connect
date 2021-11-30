from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.http.response import HttpResponseRedirect
from .models import userprofile,userverify
from django.shortcuts import render
from .form import LoginForm,RegistrationForm,updateprofile
from django.contrib.auth import get_user_model,logout,authenticate
from django.contrib.auth import login as auth_login
import uuid
from django.core.mail import send_mail
from django.conf import settings

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

                        auth_token = str(uuid.uuid4())
                        u = userverify(name=uname,token=auth_token)
                        u.save()

                        o_obj1 = obj1.save()
                        o_obj1.is_active = False
                        o_obj1.save()

                        sendemailver(email,auth_token)
                        
                        messages.success(request,"Email verification link sent to your mail...")
                else:
                    messages.error(request,"Email is already taken...")
            else:
                if obj1.is_valid():

                    auth_token = str(uuid.uuid4())
                    u = userverify(name=uname,token=auth_token)
                    u.save()

                    o_obj1 = obj1.save()
                    o_obj1.is_active = False # is_active means that is user can login or not (when it is false it treat user as inactive(or as deactivated account))
                    o_obj1.save()

                    sendemailver(email,auth_token)

                    messages.success(request,"Email verification link sent to your mail...")
        else:
            obj = LoginForm(request=request,data=request.POST)
            if obj.is_valid():
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    auth_login(request,user)
                    return HttpResponseRedirect("/home")
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

def home(request):
    if request.user.is_authenticated:
        obj = userprofile.objects.get(name=request.user)
        return render(request,"home.html",{"obj":obj})
    return HttpResponseRedirect("/")

def profile(request,id):
    print(id)
    if request.user.is_authenticated:
        us = get_user_model().objects.get(username=request.user)
        # us2 = userprofile.objects.get(name=request.user)
        # print(userprofile.objects.all()[0].id)
        if request.method == "POST":
            username = request.POST.get('username')
            bio = request.POST.get('bio')
            email = request.POST.get('email')
            phno = request.POST.get('phno')
            gender = request.POST.get('gender')
            
            us.username = username
            # us2.name = username
            us.email = email
            # us2.email = email
            # us2.bio = bio
            # us2.phoneno = phno
            # us2.gender = gender

            # us.save()
            # us2 = userprofile.objects.get(id=id)
            u = userprofile(id=id,name=username,bio=bio,email=email,phoneno=phno,gender=gender)
            u.save()
            
            # input 'name' should be equal to model name
            # u = updateprofile(request.POST,instance=us2)
            # print(u)
            # if u.is_valid():
            #     u.save()
                # messages.success(request,"Profile updated!!!")
        return render(request,"profile.html")
    return HttpResponseRedirect("/")

def changepassword(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            obj = PasswordChangeForm(user=request.user,data=request.POST)
            if obj.is_valid():
                messages.success(request,"Password Changed!!!")
                obj.save()
                return HttpResponseRedirect("/")
        else:
            obj = PasswordChangeForm(request)
        return render(request,"changepassword.html",{"form":obj})
    return HttpResponseRedirect("/")


def userlogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out!!!")
    return HttpResponseRedirect("/")

def sendemailver(email,auth_token):
    subject = "To verify email!!!"
    msg = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    receiver = [email]
    send_mail(subject,msg,email_from,receiver)

def verify_email(request,auth_token):
    obj = userverify.objects.get(token=auth_token)
    if obj:
        user = get_user_model().objects.get(username=obj.name)
        user.is_active = True
        user.save()

        obj1 = userprofile(name=user.username,email=user.email)
        obj1.save()

        messages.success(request,"Email Verified...")
        return HttpResponseRedirect("/")

    messages.error(request,"Email could not be verified...")
    return HttpResponseRedirect("/")