from django import forms
from myapplication.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter username")
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'password',)