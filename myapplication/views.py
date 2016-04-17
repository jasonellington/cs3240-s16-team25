from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from myapplication.models import Message, Report
from django.contrib.auth.models import User, Group
from myapplication.forms import UserForm, GroupForm, SendMessage, ReportForm
from datetime import datetime

# Create your views here.

def index(request):
    report_list=Report.objects.all()
    report_form=ReportForm(data=request.POST)
    if report_form.is_valid():
        report = report_form.save(user=request.user)
        report.save()
    context_dict = {'Reports' : report_list, 'report_form' : report_form}

    return render(request, 'index.html', context_dict)


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
        create_manager = True

        manager_list = User.objects.filter(is_staff=True)
        num_managers = len(manager_list)
        if num_managers > 2:
            create_manager = False


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

        context_dict = {'users': user_list, 'group_form': group_form, 'groups': group_list, 'create_manager': create_manager}

        return render(request, 'manager.html', context_dict)


    else:
        #Deploy SWAT if a non-admin tries to access the page
        return HttpResponse("A SWAT team is on the way")

def user_to_group(request):
    if request.method == 'POST':
            if request.POST.get('user-group-btn'):
                username  = request.POST.get('username')
                group_name = request.POST.get('group-name')
                try:
                    group = Group.objects.get(name=group_name)
                    group.user_set.add(User.objects.get(username=username))
                    group.save()
                except Group.DoesNotExist:
                    pass
    return HttpResponseRedirect('/myapplication/manager')


def make_manager(request):
    if request.method == 'POST':
        manager_list = User.objects.filter(is_staff=True)
        num_managers = len(manager_list)

        if request.POST.get('manager-btn'):
            username  = request.POST.get('username')
            try:
               user = User.objects.get(username=username)
               if user.is_staff:
                   user.is_staff = False
               elif num_managers < 3:
                   user.is_staff = True
               user.save()

            except User.DoesNotExist:
                pass
    return HttpResponseRedirect('/myapplication/manager')


def messaging(request):

    Messages = Message.objects.filter(recipient=request.user.username)
    # except:
    #     Messages = []
    context_dict = {'messages' : Messages}
    

    if request.method == 'POST':
        if request.POST.get('submit'):

            form = SendMessage(data=request.POST)

            if form.is_valid():
                send_message = form.save(commit=False)
                send_message.sender = request.user.username
                send_message.save()

            else:
                print(form.errors)
        if request.POST.get('delete-message'):
            

            id = request.POST.get('id')

            try:
                dump = Message.objects.get(id=id)
                dump.delete()
            except:
                print("delete failed")


    return render(request, 'messaging.html', context_dict)


def reports(request):
    report_list=Report.objects.all()
    params = []
    if request.method == 'POST':
        items = request.POST
        for item in items:
            if "cat" in item:
                num = item[3:]
                param = {"cat" : request.POST.get("cat" + str(num)),
                         "con" : request.POST.get("con" + str(num)),
                         "val" : request.POST.get("val" + str(num))}
                params.append(param)
    new_list = []
    exclude = []
    for param in params:
        con = param["con"]
        cat = param["cat"]
        val = param["val"]
        if val == "":
            continue
        if con == 'AND':
            if cat == "Description":
                for report in report_list:
                    if str(report.description) != str(val):
                        exclude.append(str(report.author) + str(report.date))
            elif cat == "Created After":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() <= date_object.date():
                        exclude.append(str(report.author) + str(report.date))
            elif cat == "Created Before":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() >= date_object.date():
                        exclude.append(str(report.author) + str(report.date))
            elif cat == "Created On":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() != date_object.date():
                        exclude.append(str(report.author) + str(report.date))
            else:
                for report in report_list:
                    if str(report.author) != str(val):
                        exclude.append(str(report.author) + str(report.date))
        else:
            if cat == "Description":
                for report in report_list:
                    if str(report.description) == str(val):
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            elif cat == "Created After":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() > date_object.date():
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            elif cat == "Created Before":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() < date_object.date():
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            elif cat == "Created On":
                date_object = datetime.strptime(val, '%b %d %Y')
                for report in report_list:
                    if report.date.date() == date_object.date():
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
            else:
                for report in report_list:
                    if str(report.author) == str(val):
                        if str(report.author) + str(report.date) in exclude:
                            exclude.remove(str(report.author) + str(report.date))
    for report in report_list:
        if str(report.author) + str(report.date) not in exclude:
            new_list.append(report)

    context_dict = {"Reports": new_list}

    return render(request, 'reports.html', context_dict)
