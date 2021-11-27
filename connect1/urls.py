from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('verify/<auth_token>',views.verify_email,name="verify")
]