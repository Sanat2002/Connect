from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.http.response import HttpResponseRedirect
from .models import userprofile,userverify
from django.shortcuts import render
from .form import LoginForm,RegistrationForm
from django.contrib.auth import get_user_model,logout,authenticate
from django.contrib.auth import login as auth_login
import uuid
from django.core.mail import send_mail
from django.conf import settings

# if in case in mongodb the document 'id'(it is not a object '_id'(default)) does not exist then , delete the whole data base and create new one 
# here 'id' is 1,2,3 not object id which is default see Blogapp documents

def login(request):
    iscreatinguser = False

    if request.method == "POST":
        email = request.POST.get("email")
        uname = request.POST.get("username")
        upass = request.POST.get("password")
        if email is not None:
            iscreatinguser = True
            obj1 = RegistrationForm(request.POST)
            # use this logic in order to check the user with this email already exist in usermodel
            if get_user_model().objects.all():
                if len(get_user_model().objects.filter(email=email))==0:
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
        user = userprofile.objects.get(name=request.user)
        userposts = user.posts

        # changing the name store in db to its objects
        connectionrequests = []
        if user.connectionrequests:
            for req in user.connectionrequests:
                u = userprofile.objects.get(name=req)
                connectionrequests.append(u)

        usersuggestions = list(userprofile.objects.all())
        usersuggestions.remove(user)

        return render(request,"home.html",{"user":user,"usersuggestions":usersuggestions,"userposts":userposts,"connectionrequests":connectionrequests})
    return HttpResponseRedirect("/")

def profile(request):
    if request.user.is_authenticated:
        us = get_user_model().objects.get(username=request.user)
        us2 = userprofile.objects.get(name=request.user)
        if request.method == "POST":
            username = request.POST.get('username')
            bio = request.POST.get('bio')
            email = request.POST.get('email')
            phno = request.POST.get('phno')
            gender = request.POST.get('gender')
            if len(request.FILES) != 0: # to check if any file is selected or not
                profilepic = request.FILES['profilepic'] # add enctype="multipart/form-data" in form in html file in case of uploading files 
                print(profilepic.size) # size of file
                print(profilepic.name) # return name as string
            else:
                profilepic = us2.profile_pic
            
            us.username = username
            us.email = email
            us.save()

            u = userprofile(id=us2.id,name=username,bio=bio,email=email,phoneno=phno,gender=gender,profile_pic=profilepic,posts=us2.posts)
            u.save()
            us2 = userprofile.objects.get(name=username)
            print(us2.profile_pic.url)
            messages.success(request,"Profile updated!!!")            
        return render(request,"profile.html",{"user":us2})
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

def posts(request):
    if request.user.is_authenticated:
        user = userprofile.objects.get(name=request.user)
        posts = user.posts
        if request.method == "POST":
            user.toaddpost = request.FILES['addimage']
            user.save()
            if type(user.posts) == list:
                lst = list(user.posts)
                lst.append(user.toaddpost.name) # user.toaddpost.name is used because jsonField does not store imageField object
                user.posts = lst
            else:
                user.posts = [user.toaddpost.name]
            user.save()
            messages.success(request,"Post Uploaded!!!")
            posts = user.posts
        return render(request,'posts.html',{"posts":posts})
    return HttpResponseRedirect("/login")

def deletepost(request,postid):
    if request.user.is_authenticated:
        user = userprofile.objects.get(name=request.user)
        lst = list(postid)
        lst.insert(7,"/")
        postid = "".join(lst)
        lst2 = user.posts
        lst2.remove(postid)
        user.posts = lst2
        user.save()
        return HttpResponseRedirect("/posts")
    return HttpResponseRedirect("/")

def sendconnectionreq(request,name):
    user = userprofile.objects.get(name=request.user)
    reqsendtouser = userprofile.objects.get(name=name)
    if type(reqsendtouser.connectionrequests) == list:
        lst = list(reqsendtouser.connectionrequests)
        lst.append(user.name)
        reqsendtouser.connectionrequests = lst
    else:
        reqsendtouser.connectionrequests = [user.name]
    
    reqsendtouser.save()
    return HttpResponseRedirect("/home")

def acceptconnectionreq(request,name):
    user = userprofile.objects.get(name=request.user)
    reqsenduser = userprofile.objects.get(name=name)

    if type(user.connections) == list:
        lst = list(user.connections)
        lst.append(reqsenduser.name)
        user.connections = lst
    else:
        user.connections = [reqsenduser.name]
    
    if type(reqsenduser.connections) == list:
        lst = list(reqsenduser.connections)
        lst.append(user.name)
        reqsenduser.connections = lst
    else:
        reqsenduser.connections = [user.name]
    
    user.save()
    reqsenduser.save()
    return HttpResponseRedirect("/home")

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