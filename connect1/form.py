from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets

class RegistrationForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({
            'name':'username',
            'class':'col-11','style':'border-radius: .5vw;height: 2.5vw;margin-bottom: 1.8vw; border-color: rgb(200, 202, 204);','placeholder':'Enter email'
        })

    class Meta:
        model = User

        fields = '__all__'

        # widgets = {'username':forms.EmailInput(attrs={'class':'col-11','style':'border-radius: .5vw;height: 2.5vw;margin-bottom: 1.8vw; border-color: rgb(200, 202, 204);','placeholder':'Enter email'})}