from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render
from .form import RegistrationForm

# use your own customized form and just take the value from inputs and pass value to the django authentication form to authenticate 

def login(request):
    # user = RegistrationForm()
    if request.method == "POST":
        name = request.POST.get("email")
        pas = request.POST.get("password")
        user = RegistrationForm(request.POST)
        if user.is_valid():
            print(name,pas)
            # user.save()
    else:
        user = RegistrationForm()
    return render(request,"login.html",{"form":user})