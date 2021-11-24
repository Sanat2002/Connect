from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# use your own customized form and just take the value from inputs and pass value to the django authentication form to authenticate 

def login(request):
    if request.method == "POST":
        name = request.POST.get("email")
        pas = request.POST.get("password")
        user = UserCreationForm(username="ks",first_name="sanat",last_name="ksksss",email=name,password=pas)
        if user.is_valid():
            print(name,pas)
            user.save()
    return render(request,"login.html")