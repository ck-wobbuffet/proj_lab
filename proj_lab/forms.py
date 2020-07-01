from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


placeholder_account = 'please input your username'
placehodler_passwd = 'please input your password'
placeholder_email = 'please input your email'

class LoginForm(forms.Form):
    
    username = forms.CharField(label='username',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': placeholder_account+' or register'}),
                                required=True)  # false表示不需要填写
    password = forms.CharField(label='password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': placehodler_passwd}))
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Wrong password or account!')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='username',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': placeholder_account}),
                                max_length=15,
                                min_length=2,
                                required=True)  # false表示不需要填写
    password = forms.CharField(label='password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': placehodler_passwd}),
                                max_length=20,
                                min_length=6)
    password_again = forms.CharField(label='password again',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': placehodler_passwd + ' again'}),
                                max_length=20,
                                min_length=6)
    email = forms.EmailField(label='email',
                                widget=forms.EmailInput(attrs={'class':'form-control','placeholder':placeholder_email}))
            
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists!')
        return username

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        return email


    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('Passwords entered twice are inconsistent!')
        return password_again
