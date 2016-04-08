from django import forms
from django.contrib.auth.models import User
from myapplication.models import Message


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class SendMessage(forms.ModelForm):

    # recipient = forms.CharField(max_length=30)
    # message = forms.TextInput()


    class Meta:
        model = Message
        fields = ('recipient', 'message')