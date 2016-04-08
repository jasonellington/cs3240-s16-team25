from django import forms
from django.contrib.auth.models import User
from myapplication.models import Message

from django.contrib.auth.models import User, Group


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
class GroupForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Group
        fields = ('name',)


