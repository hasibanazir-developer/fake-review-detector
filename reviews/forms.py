# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Custom LoginForm based on AuthenticationForm
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Custom RegistrationForm based on UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)


class ReviewForm(forms.Form):
    review_text = forms.CharField(widget=forms.Textarea, max_length=1000, label='Your Review')
