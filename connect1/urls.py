from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('verify/<auth_token>',views.verify_email,name="verifyemail"),
    path('home',views.home,name="home"),
    path('profile',views.profile,name="profile"),
    path('changepassword',views.changepassword,name="changepassword"),
    path('posts',views.posts,name="posts"),
    path('deletepost/<postid>',views.deletepost,name="deletepost"),
    path('sendconnectionreq/<name>',views.sendconnectionreq,name="sendconnectionreq"),
    path('acceptconnectionreq/<name>',views.acceptconnectionreq,name="acceptconnectionreq"),
    path('rejectconnectionreq/<name>',views.rejectconnectionreq,name="rejectconnectionreq"),
    path('breakconnection/<name>',views.breakconnection,name="breakconnection"),
    path('deletependingconnection/<name>',views.deletependingconnection,name="deletependingconnection"),
    path('showprofile/<name>',views.showprofile,name="showprofile"),
    path('delacc',views.deleteaccount,name="delacc"),
    path('logout',views.userlogout,name="logout"),
]