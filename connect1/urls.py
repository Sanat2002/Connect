from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('verify/<auth_token>',views.verify_email,name="verifyemail"),
    path('home',views.home,name="home"),
    path('profile',views.profile,name="profile"),
    path('changepassword',views.changepassword,name="changepassword"),
    path('logout',views.userlogout,name="logout"),
]