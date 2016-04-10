from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from myapplication.models import Message

from myapplication.forms import UserForm, SendMessage
from django.contrib.auth.models import User, Group


from myapplication.forms import UserForm, GroupForm


# Create your views here.

def index(request):
    return render(request, 'index.html')


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                if (user.is_staff):
                    login(request,user)
                    return HttpResponseRedirect('/myapplication/manager/')
                login(request, user)
                return HttpResponseRedirect('/myapplication/')
            else:
                return HttpResponse("Your account is disabled")

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('login.html', {}, context)


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render_to_response('register.html', {'user_form': user_form, 'registered': registered},
                              context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/myapplication/')


def manager(request):
    if request.user.is_staff:
        user_list = User.objects.all()
        group_list = Group.objects.all()
        group_form = GroupForm()

        if request.method == 'POST':
            if request.POST.get('suspend-btn'):
                username  = request.POST.get('username')
                try:
                    user = User.objects.get(username=username)
                    if user.is_active:
                        user.is_active = False
                    else:
                        user.is_active = True
                    user.save()
                except User.DoesNotExist:
                    pass
            else:
                group_form = GroupForm(data=request.POST)
                if group_form.is_valid():
                    group = group_form.save()
                    group.save()

        context_dict = {'users': user_list, 'group_form': group_form, 'groups': group_list}

        return render(request, 'manager.html', context_dict)


    else:
        #Deploy SWAT if a non-admin tries to access the page
        return HttpResponse("A SWAT team is on the way")


def messaging(request):

    Messages = Message.objects.filter(recipient=request.user.username)
    # except:
    #     Messages = []
    context_dict = {'messages' : Messages}
    

    if request.method == 'POST':
        form = SendMessage(data=request.POST)

        if form.is_valid():
            send_message = form.save(commit=False)
            send_message.sender = request.user.username
            send_message.save()

        else:
            print(form.errors)


    return render(request, 'messaging.html', context_dict)
