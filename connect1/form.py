from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets

class LoginForm(AuthenticationForm):

    # this is how we can give attr to the fields
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({
            'class':'col-11','style':'border-radius: .5vw;height: 2.5vw;margin-bottom: 1vw; margin-left:.7vw; border-color: rgb(200, 202, 204);','placeholder':'Enter email'
        })
        self.fields['password'].widget.attrs.update({
            'class':'col-11','style':'border-radius: .5vw;height: 2.5vw;margin-bottom: 1.6vw; margin-left:.7vw; border-color: rgb(200, 202, 204);','placeholder':'Password'
        })


    class Meta:
        model = User

        fields = '__all__'
        labels = {"username":"Userkname"}
        

