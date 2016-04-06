from django import forms
from django.contrib.auth.models import User, Group


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class GroupForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Group
        fields = ('name',)