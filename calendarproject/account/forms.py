from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import widgets
from .models import CustomUser
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"username",
         "placeholder":"username",
     }),label="Username", error_messages={'unique' : '입력하신 이름을 사용하는 유저가 이미 존재합니다',
                                            'max_length' : '이름은 최대 150글자까지 작성할 수 있습니다'})

    password1 = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"password",
         "placeholder":"enter password",
     }),label="password")

    password2 = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"password",
         "placeholder":"confirm password",
     }),label="password")

    nickname = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"nickname",
         "placeholder":"nickname",
     }),label="enter nickname", error_messages={'unique' : '입력하신 닉네임을 사용하는 유저가 이미 존재합니다'})

    email = forms.CharField(widget = forms.TextInput(attrs={
         "class":"input",
         "type":"email",
         "placeholder":"email",
     }),label="enter email")

    error_messages = {
        'password_mismatch': '입력하신 두 비밀번호가 같지 않습니다',
    }

    profile = forms.ImageField(widget = forms.FileInput(attrs={
         "class":"input",
         "type":"file",
     }),label="upload profile")

    class Meta:
        model = CustomUser
        fields = ['username','password1','password2','nickname','email', 'profile']
    
    # def clean_password2(self):
    #     password = self.cleaned_data.get('password2')
    #     if len(password) < 8:
    #         raise ValidationError("비밀번호는 최소 8글자 이상이어야 합니다")
    #     return password