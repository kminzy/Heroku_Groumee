from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import widgets
from .models import CustomUser

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"username",
         "placeholder":"username",
     }),label="Username")

    password1 = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"password",
         "placeholder":"enter password",
     }),label="password")

    password2 = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"password",
         "placeholder":"enter password",
     }),label="password")

    nickname = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"nickname",
         "placeholder":"nickname",
     }),label="enter nickname")

    email = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"email",
         "placeholder":"email",
     }),label="enter email")

    class Meta:
        model = CustomUser
        fields = fields = ['username','password1','password2','nickname','email']