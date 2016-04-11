from django import forms
from django.forms import ModelForm
from myapplication.models import Message,Report
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

class ReportForm(forms.ModelForm):
    description = forms.CharField(max_length=128,help_text="Enter a short description")
    content = forms.TextInput()
    security = forms.BooleanField(required=False, initial=False, label="Private")

    def save(self,user, commit=True):
        r = ModelForm.save(self,commit=False)
        r.author = user
        if commit:
            r.save()
        return r

    class Meta:
        model = Report
        fields = ('description','content','security')